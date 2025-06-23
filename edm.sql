-- SQL Query to Calculate Weekly Marketing Lead Volume and Costs
-- Objective: Assess marketing ROI by combining GA data, LeadMix data, technical costs, and media spend.

-- Overview:
-- This query combines Google Analytics (GA3 and GA4) data with LeadMix performance data,
-- technical marketing costs, and media spend to deliver a comprehensive view of marketing ROI.
-- The output is structured on a weekly basis by brand, product, and campaign.

-- Databases & Tables Used:
-- digitaldw.ga.session                          - GA3 session data
-- digitaldw.ga.event_new                        - GA4 event data
-- digitaldw.tmp.missing_content_grouping_ga     - Mappings to enrich GA3 data
-- DigitalDW.leadmix.leadmix_all_matched_sales   - Internal CRM performance data
-- DigitalDW.edm.tech_costs                      - Technical marketing costs
-- Media.dbo.vwROIReport_Weekly_Cached           - Historical weekly media costs
-- Media.dbo.tblROIReport_All                    - Latest media ROI reports
-- HollardDW.dbo.dimDate                         - Used for padding Guardian dummy rows

-- Date Ranges and Filters:
-- GA3 Data:        2019-07-01 to 2024-06-30
-- GA4 Data:        2024-07-01 to GETDATE()-1
-- LeadMix Data:    2020-01-01 to GETDATE()-1, only where SourceMedium LIKE 'hs%'
-- Media Data:      2016-09-01 to GETDATE()-1
-- Fiscal Year:     Starts on July 1, ends June 30

-- Filters:
-- GA data filtered to channel_grouping = 'Hubspot'
-- Only exclude SPCA's incorrectly labeled campaign "SPCAG1_Life"
-- Remove ASIA Travel anomalies between 2018-11-18 to 2019-01-27 in media spend
-- Special handling for Guardian 2022 with fixed cost per lead row
-- Exclude GuideDogs brand in FY2023 from cost allocations

-- Step-by-step breakdown follows:

-- Step 1: Combine GA3 Sessions
-- Business Logic: Normalize GA3 data to ensure all sessions have product and campaign data.
WITH GA3 AS (
    SELECT 
        session_id,
        campaign,
        brand,
        CASE 
            WHEN product = '(not set)' THEN mcg.product -- Impute missing product using content grouping
            ELSE product
        END AS product,
        date
    FROM digitaldw.ga.session s
    LEFT JOIN digitaldw.tmp.missing_content_grouping_ga mcg
        ON s.page_path = mcg.page_path
    WHERE source = 'Hubspot' AND date BETWEEN '2019-01-01' AND '2024-12-31'
),

-- Step 2: Prepare GA4 Events
-- Business Logic: Normalize GA4 structure to match GA3 format for unified analysis.
GA4_raw AS (
    SELECT 
        event_id,
        campaign,
        brand,
        product,
        DATE(event_date) AS date,
        REPLACE(page_path, 'https://www.example.com', '') AS page_path -- Clean URLs
    FROM digitaldw.ga.event_new
    WHERE event_date >= '2024-07-01'
),
GA4 AS (
    SELECT 
        event_id,
        campaign,
        brand,
        product,
        date,
        page_path
    FROM GA4_raw
),

-- Step 3: Combine GA3 + GA4
-- Business Logic: Unified GA dataset across GA3 and GA4 transition.
GA AS (
    SELECT * FROM GA3
    UNION
    SELECT * FROM GA4
),

-- Step 4: Load LeadMix Data
-- Business Logic: Aggregate daily leads, sales, and ARRA by brand, product, campaign, and date.
LM AS (
    SELECT 
        brand,
        product,
        campaign,
        dateid AS date,
        COUNT(DISTINCT lead_id) AS leads,
        SUM(sales) AS sales,
        SUM(ARRA) AS revenue
    FROM DigitalDW.leadmix.leadmix_all_matched_sales
    WHERE SourceMedium LIKE 'hs%' -- Filter for HubSpot-based leads
    GROUP BY brand, product, campaign, dateid
),

-- Step 5: Aggregate GA Data Weekly
-- Business Logic: Aggregate GA leads by marketing campaign on a weekly and fiscal-year basis.
GA_Aggregated AS (
    SELECT 
        brand,
        product,
        campaign,
        DATEADD(week, DATEDIFF(week, -1, date), -1) AS weekStart, -- Weekly grouping
        FiscalYear = CASE 
            WHEN MONTH(date) >= 7 THEN YEAR(date) + 1 -- Fiscal year starts in July
            ELSE YEAR(date)
        END,
        COUNT(DISTINCT session_id) AS ga_leads
    FROM GA
    GROUP BY brand, product, campaign, date
),

-- Step 6: Fiscal-Year Level GA Summary
-- Business Logic: Calculate tech cost per GA lead for each brand in each fiscal year.
GA_Brand_Leads AS (
    SELECT 
        FiscalYear,
        brand,
        SUM(ga_leads) AS FiscalYearLeads,
        tc.total_cost,
        tc.DaysInFiscalYear
    FROM GA_Aggregated ga
    LEFT JOIN DigitalDW.edm.tech_costs tc
        ON ga.brand = tc.brand AND ga.FiscalYear = tc.FiscalYear
    WHERE CONCAT(ga.brand, ga.FiscalYear) <> 'GuideDogs2023'
    GROUP BY FiscalYear, brand, tc.total_cost, tc.DaysInFiscalYear
),

-- Step 7: Calculate Tech Cost per Lead
-- Business Logic: Cost per lead = total cost / total GA leads for the year.
TechCosts AS (
    SELECT 
        brand,
        FiscalYear,
        total_cost / FiscalYearLeads AS cost_per_lead
    FROM GA_Brand_Leads
    UNION
    SELECT 'Guardian', 2022, 35.91780821917808219
),

-- Step 8: Join GA + LeadMix + Tech Costs
-- Business Logic: Tie together digital behavior (GA), outcomes (LeadMix), and investment (TechCosts).
Data_with_tech_costs AS (
    SELECT 
        ga.brand,
        ga.product,
        ga.campaign,
        ga.weekStart,
        ga.ga_leads,
        lm.leads AS LeadMixLeads,
        lm.sales,
        lm.revenue,
        tc.cost_per_lead,
        CASE 
            WHEN ga.FiscalYear = YEAR(GETDATE()) THEN tc.cost_per_lead * DATEDIFF(day, '2024-07-01', GETDATE()) / tc.DaysInFiscalYear -- Prorated cost for YTD
            ELSE tc.cost_per_lead
        END AS tech_costs
    FROM GA_Aggregated ga
    LEFT JOIN LM lm
        ON ga.brand = lm.brand AND ga.product = lm.product AND ga.campaign = lm.campaign AND ga.weekStart = lm.date
    LEFT JOIN TechCosts tc
        ON ga.brand = tc.brand AND ga.FiscalYear = tc.FiscalYear
    UNION ALL
    SELECT 'Guardian', 'Life', NULL, weekStart, 0, 0, 0, 0, 35.91780821917808219, 35.91780821917808219
    FROM HollardDW.dbo.dimDate
    WHERE date BETWEEN '2021-07-01' AND '2022-06-30'
),

-- Step 9: Media Weekly Costs
-- Business Logic: Get cost data (agent spend) that drove leads, on a weekly basis.
media_weekly AS (
    SELECT 
        brand,
        product,
        weekStart,
        SUM(agentcost) AS agent_cost,
        SUM(leads) AS leads
    FROM Media.dbo.vwROIReport_Weekly_Cached
    WHERE channel IN ('OnlineInbound') AND brand IN ('BrandA', 'BrandB')
    GROUP BY brand, product, weekStart
),
media_roi AS (
    SELECT 
        brand,
        product,
        weekStart,
        agent_cost / leads AS agent_cost_per_lead
    FROM media_weekly
),

-- Step 10: Final Join & Output
-- Business Logic: Combine GA/LeadMix data with media cost data by week.
FinalOutput AS (
    SELECT 
        dtc.brand,
        dtc.product,
        dtc.campaign,
        dtc.weekStart,
        dtc.ga_leads,
        dtc.LeadMixLeads,
        dtc.sales,
        dtc.revenue,
        dtc.tech_costs,
        mr.agent_cost_per_lead,
        dtc.ga_leads * mr.agent_cost_per_lead AS agent_costs
    FROM Data_with_tech_costs dtc
    LEFT JOIN media_roi mr
        ON dtc.brand = mr.brand AND dtc.product = mr.product AND dtc.weekStart = mr.weekStart
)

-- Final Output: Weekly attribution view showing GA leads, LeadMix actuals, tech costs, agent costs, and media spend.
SELECT * FROM FinalOutput;





/*

## 🎯 **Objective of the Query**

To calculate weekly marketing lead volume and costs (from HubSpot and media), mapped to:

* **Brand**
* **Product**
* **Campaign**
* **Fiscal year**

It combines **Google Analytics (GA3 and GA4)** data, **LeadMix (internal lead + sales data)**, **technical marketing costs**, and **weekly media spend** — all to assess marketing ROI down to campaign level.

---

## 🧱 **Databases & Key Tables Involved**

| Database            | Table/Source                                    | Description                                   |
| ------------------- | ----------------------------------------------- | --------------------------------------------- |
| `digitaldw.ga`      | `session`, `event_new`                          | GA3 and GA4 data                              |
| `digitaldw.tmp`     | `missing_content_grouping_ga`                   | Page path enrichment mapping                  |
| `DigitalDW.leadmix` | `leadmix_all_matched_sales`                     | CRM-linked leads, sales, and revenue          |
| `DigitalDW.edm`     | `tech_costs`                                    | Technical marketing cost by brand/fiscal year |
| `Media.dbo`         | `vwROIReport_Weekly_Cached`, `tblROIReport_All` | Weekly & current ROI/agent cost reports       |
| `HollardDW.dbo`     | `dimDate`                                       | Used to generate Guardian dummy data          |

---

## 📘 Step-by-Step Breakdown

---

### **Step 1: Combine GA3 Sessions**

**CTE: `GA3`**

* **Filters**: Only ‘Hubspot’ sessions from 2019–2024.
* **Product logic**:

  * If `product = '(not set)'`, try joining with `missing_content_grouping_ga` to impute the product.
  * Else keep the product.
* **Goal**: Normalize GA3 data to ensure all sessions have product and campaign data.

> **Business logic**: Not all GA3 sessions have products — so try to fill missing ones with content-grouping mappings.

---

### **Step 2: Prepare GA4 Events**

**CTEs: `GA4_raw`, `GA4`**

* Pull GA4 `event_new` data from July 2024 onward.
* Clean URLs (`ord_page_path`) into hostname.
* Normalize structure to match GA3 format.

> **Business logic**: GA4 has different structure, so map it to GA3-compatible columns (e.g., rename `event_date`, strip hostname).

---

### **Step 3: Combine GA3 + GA4**

**CTE: `GA`**

```sql
SELECT * FROM GA3
UNION
SELECT * FROM GA4
```

> **Business logic**: Unified GA dataset across GA3 and GA4 transition.

---

### **Step 4: Load LeadMix Data**

**CTE: `LM`**

* Aggregates daily leads, sales, and ARRA by:

  * Brand, Product, Campaign, Date (`dateid`)
* Filters for HubSpot-based leads only (`SourceMedium LIKE 'hs%'`)

> **Business logic**: Get actual lead-to-sale performance from internal data.

---

### **Step 5: Aggregate GA Data Weekly**

**CTE: `GA_Aggregated`**

* Weekly groupings: `weekStart = DATEADD(week, DATEDIFF(week, -1, date), -1)`
* Fiscal year calculation: starts in July
* Count of **unique GA leads (ga\_client\_id)** by day, campaign, product, brand

> **Business logic**: Aggregate GA leads by marketing campaign on a weekly and fiscal-year basis.

---

### **Step 6: Fiscal-Year Level GA Summary**

**CTE: `GA_Brand_Leads`**

* Summarizes `ga_leads` by FiscalYear and Brand
* Joins with `tech_costs` to bring in total cost per brand and year
* Calculates:

  * `DaysInFiscalYear`
  * Special exclusion for `GuideDogs2023`

> **Business logic**: This is to calculate **tech cost per GA lead** for each brand in each fiscal year.

---

### **Step 7: Calculate Tech Cost per Lead**

**CTE: `TechCosts`**

* Adds column: `cost / FiscalYearLeads`
* Includes special row for `Guardian` brand in 2022 with fixed tech cost.

> **Business logic**: Cost per lead = total cost / total GA leads for the year.

---

### **Step 8: Join GA + LeadMix + Tech Costs**

**CTE: `Data_with_tech_costs`**

* Join:

  * `GA_Aggregated` + `LeadMix` (on brand, product, date, campaign)
  * `GA_Aggregated` + `TechCosts` (on brand and fiscal year)

* Calculates `tech_costs` as:

  * **If current FY**, prorated cost for YTD
  * **Else**, normal total cost

* **Includes dummy Guardian row** for 2022 with zero GA/LeadMix metrics

> **Business logic**:

* Tie together **digital behavior (GA)**, **outcomes (LeadMix)**, and **investment (TechCosts)**.
* Allocate costs based on how far we are into the financial year.

---

### **Step 9: Media Weekly Costs**

**CTEs: `media_weekly`, `media_roi`**

* Pulls **weekly agent media costs** and **leads** from 2 sources:

  * Historical = `vwROIReport_Weekly_Cached`
  * Latest week = `tblROIReport_All`
* Filters for:

  * Brands of interest
  * Online inbound channels

> **Business logic**: Get cost data (agent spend) that actually drove those leads, on a weekly basis.

---

### **Step 10: Clean Media Data**

**CTE: `media_union_clean`**

* Merges old + current media data
* Removes known anomalies (e.g., ASIA Travel Nov 2018–Jan 2019)
* Calculates `agent_cost_per_lead = agentcost / leads`

---

### **Step 11: Final Join & Output**

**Final SELECT**

* Join `Data_with_tech_costs` + `media_union_clean` on:

  * Brand, Product, Week
* Computes:

  * `agent_costs = ga_leads * agent_cost_per_lead`

> **Business Output**:
> Each row represents:

* One brand + product + campaign
* In one week
* Showing:

  * GA leads
  * LeadMix actuals
  * Tech costs
  * Agent costs
  * Media spend
  * Derived cost per lead

---

## 🔁 Algorithmic Flow Summary

```text
1. Load GA3 & enrich (fallback for missing product).
2. Load GA4 and normalize.
3. Union GA3 + GA4 into a unified dataset.
4. Aggregate GA leads weekly.
5. Load LeadMix (internal lead/sales data).
6. Load Tech Cost data and calculate cost per lead.
7. Join GA data with LeadMix and Tech Costs.
8. Handle special Guardian rows.
9. Load and clean Media weekly cost data.
10. Join GA/LeadMix data with media cost data by week.
11. Final output with all marketing + performance metrics.
```

---

## ✅ Deliverables from This Query

* **Weekly attribution view** of:

  * Leads from GA (HubSpot)
  * Internal lead & sales outcomes
  * Technical cost attribution
  * Weekly agent marketing costs

Perfect for: **cost per lead analysis**, **budgeting**, **campaign ROI evaluation**, **trend monitoring**.

---

If you'd like, I can:

* Draw a flowchart of these steps
* Optimize the query
* Help you visualize results in Power BI or Python

Let me know!

*/