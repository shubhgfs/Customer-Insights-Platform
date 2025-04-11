# [HollardDW].[dbo].[FactSalesActivity]

```sql
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [SourceSystemID]
      ,[DateID]
      ,[QuoteID]
      ,[RiderCode]
      ,[ProductCode]
      ,[UserID]
      ,[ClientID]
      ,[BrandID]
      ,[ClientSourceID]
      ,[ClientWorkItemID]
      ,[ClientGNCStepDesc]
      ,[QuoteSourceID]
      ,[QuoteWorkItemID]
      ,[ProductSetID]
      ,[ChannelID]
      ,[ChannelID_PartnerReporting]
      ,[CampaignBatchID]
      ,[IsMedibankMember]
      ,[Sales]
      ,[Premium]
      ,[InceptionEV]
      ,[NPV_Gross_HFS_Comm]
      ,[NPV_Insurer_Upfront]
      ,[NPV_Insurer_Trail]
      ,[NPV_Partner_Upfront]
      ,[NPV_Partner_Trail]
      ,[NPV_SalesIncentive_Upfront]
      ,[NPV_SalesIncentive_Trail]
      ,[NPV_RealLiability]
      ,[CollectionDelay]
      ,[LivesSold]
      ,[LivesSold_Actual]
      ,[Riders]
      ,[Rider_Premium]
      ,[SumInsured]
      ,[Quotes]
      ,[Applications]
      ,[CommissionCode]
      ,[CommissionPremium]
      ,[RetainedPremium]
      ,[ClientResponseID]
      ,[QuoteResponseID]
      ,[RUWDaysPending]
      ,[DWdtmInserted]
      ,[DWdtmUpdated]
      ,[DWStatusID]
      ,[Commission]
      ,[ProductTypeID]
      ,[SaleDateTimeID]
      ,[PremiumWithLoading]
      ,[BenefitSumInsured]
      ,[RecommendedBenefitSumInsured]
      ,[RecommendedRiderCode]
      ,[NPV_HAS_Comm]
      ,[ClientPolicyNumber]
      ,[PolicyStatusID]
      ,[dtmFirstCollection]
      ,[dtmLapseOrCancelDate]
      ,[PaymentMethodID]
      ,[PaymentMethod]
      ,[dtmPaidUpto]
      ,[60DaysDateID]
      ,[CurrentPremium]
      ,[dtmDeclaration]
      ,[dtmFirstPayment]
      ,[ARRA_Statutory]
      ,[ARRA_Management]
      ,[PartnerID]
      ,[MembershipID]
      ,[ARRA]
      ,[ClientBrandID]
      ,[SaleTimeID]
      ,[TripTypeID]
      ,[TripType]
      ,[StoreStars]
      ,[SystemID]
      ,[QuoteDateTimeID]
      ,[ConversionPeriod]
      ,[ProductGroupID]
      ,[AUDCurrencyRate]
  FROM [HollardDW].[dbo].[FactSalesActivity]
```

## Table Description

The `FactSalesActivity` table is the primary fact table that captures all sales activity data for insurance products. It contains comprehensive information about quotes, applications, sales, premiums, commissions, and policy details. This table serves as the central repository for sales analytics and financial reporting.

## Column Descriptions

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| SourceSystemID | int | Identifies the source system from which the data originated. Predominantly values 1 and 2 as seen in data overview. |
| DateID | date | The date associated with the sales activity record. |
| QuoteID | varchar | Unique identifier for the quote. Acts as a primary identifier for sales records. |
| RiderCode | varchar | Code identifying the rider type (e.g., 'DTH' for Death, 'NOR' for Normal). |
| ProductCode | varchar | Unique code identifying the insurance product (e.g., 'FEP'). |
| UserID | varchar | ID of the user/salesperson who processed the sale or quote. |
| ClientID | int | Unique identifier for the client/customer. |
| BrandID | int | Identifier for the brand under which the sale was made. |
| ClientSourceID | int | Identifies the source from which the client was acquired. |
| ClientWorkItemID | int | Internal workflow ID for client-related processes. |
| ClientGNCStepDesc | varchar | Description of the client's position in the sales pipeline (e.g., 'STP' for Straight Through Processing). |
| QuoteSourceID | int | Identifies the source channel of the quote. |
| QuoteWorkItemID | int | Internal workflow ID for quote-related processes. |
| ProductSetID | int | Identifier for a group of related products. |
| ChannelID | int | Identifier for the sales channel used. |
| ChannelID_PartnerReporting | int | Partner-specific channel ID for segmented reporting. |
| CampaignBatchID | int | Identifier for the marketing campaign batch associated with the sale. |
| IsMedibankMember | bit | Flag indicating if the client is a Medibank member (0=No, 1=Yes). |
| Sales | decimal | Count of successful sales (typically 0 or 1). |
| Premium | decimal | The premium amount for the policy. |
| InceptionEV | decimal | Expected Value at policy inception. |
| NPV_Gross_HFS_Comm | decimal | Net Present Value of gross commission for HFS. |
| NPV_Insurer_Upfront | decimal | Net Present Value of upfront payments to the insurer. |
| NPV_Insurer_Trail | decimal | Net Present Value of trailing payments to the insurer. |
| NPV_Partner_Upfront | decimal | Net Present Value of upfront payments to partners. |
| NPV_Partner_Trail | decimal | Net Present Value of trailing payments to partners. |
| NPV_SalesIncentive_Upfront | decimal | Net Present Value of upfront sales incentives. |
| NPV_SalesIncentive_Trail | decimal | Net Present Value of trailing sales incentives. |
| NPV_RealLiability | decimal | Net Present Value of the actual liability associated with the policy. |
| CollectionDelay | int | Days of delay in premium collection. |
| LivesSold | int | Count of lives covered by the policy for reporting purposes. |
| LivesSold_Actual | int | Actual count of lives covered by the policy. |
| Riders | int | Count of additional riders attached to the policy. |
| Rider_Premium | decimal | Premium amount specific to riders. |
| SumInsured | decimal | Total sum insured amount of the policy. |
| Quotes | int | Binary indicator if this record represents a quote (0/1). |
| Applications | int | Binary indicator if this record represents an application (0/1). |
| CommissionCode | varchar | Code representing the commission structure applied. |
| CommissionPremium | decimal | Premium amount used for commission calculation. |
| RetainedPremium | decimal | Premium amount retained after deductions. |
| ClientResponseID | int | Identifier for client responses to communications. |
| QuoteResponseID | int | Identifier for quote responses or interactions. |
| RUWDaysPending | int | Days the application was pending in underwriting. |
| DWdtmInserted | datetime | Timestamp when the record was inserted into the data warehouse. |
| DWdtmUpdated | datetime | Timestamp when the record was last updated in the data warehouse. |
| DWStatusID | int | Status of the record in the data warehouse. |
| Commission | decimal | Total commission amount for the sale. |
| ProductTypeID | int | Identifier for the product type category. |
| SaleDateTimeID | datetime | Date and time when the sale was completed. |
| PremiumWithLoading | decimal | Premium amount including loading charges. |
| BenefitSumInsured | decimal | Sum insured amount for specific benefits. |
| RecommendedBenefitSumInsured | decimal | System-recommended sum insured amount for benefits. |
| RecommendedRiderCode | decimal | System-recommended rider code (stored as decimal). |
| NPV_HAS_Comm | varchar | Net Present Value of HAS commission, also used as policy identifier in some cases. |
| ClientPolicyNumber | varchar | Policy number assigned to the client. |
| PolicyStatusID | int | Status of the policy (NULL, 20, 30, 40, 50, 60, 61, 70 representing different states). |
| dtmFirstCollection | datetime | Date and time of the first premium collection. |
| dtmLapseOrCancelDate | datetime | Date and time when the policy lapsed or was cancelled. |
| PaymentMethodID | int | Identifier for the payment method used. |
| PaymentMethod | varchar | Description of the payment method (Cheque, Credit Card, Direct Debit). |
| dtmPaidUpto | datetime | Date to which premiums have been paid. |
| 60DaysDateID | date | Date representing 60 days from a reference point (possibly for reporting or collection). |
| CurrentPremium | decimal | Current premium amount as of the most recent update. |
| dtmDeclaration | datetime | Date when policy declarations were completed. |
| dtmFirstPayment | datetime | Date and time of the first payment received. |
| ARRA_Statutory | decimal | Statutory Annual Renewable Risk Amount. |
| ARRA_Management | decimal | Management Annual Renewable Risk Amount. |
| PartnerID | int | Identifier for the partner involved in the sale. |
| MembershipID | varchar | Identifier for membership programs. |
| ARRA | decimal | Total Annual Renewable Risk Amount. |
| ClientBrandID | int | Brand identifier specific to the client. |
| SaleTimeID | time | Time of day when the sale was completed. |
| TripTypeID | int | Identifier for trip type (for travel insurance). |
| TripType | varchar | Description of the trip type. |
| StoreStars | varchar | Store rating or classification. |
| SystemID | int | Identifier for the system that processed the transaction. |
| QuoteDateTimeID | datetime | Date and time when the quote was created. |
| ConversionPeriod | int | Period taken to convert from quote to sale. |
| ProductGroupID | int | Identifier for product grouping or category. |
| AUDCurrencyRate | decimal | Exchange rate to Australian Dollar if applicable. |

## Sample Data

| SourceSystemID | DateID     | QuoteID     | RiderCode | ProductCode | UserID    | ClientID | BrandID | ClientSourceID | ClientWorkItemID | ClientGNCStepDesc | QuoteSourceID | QuoteWorkItemID | ProductSetID | ChannelID | ChannelID_PartnerReporting | CampaignBatchID | IsMedibankMember | Sales | Premium   | InceptionEV | NPV_Gross_HFS_Comm | NPV_Insurer_Upfront | NPV_Insurer_Trail | NPV_Partner_Upfront | NPV_Partner_Trail | NPV_SalesIncentive_Upfront | NPV_SalesIncentive_Trail | NPV_RealLiability | CollectionDelay | LivesSold | LivesSold_Actual | Riders | Rider_Premium | SumInsured | Quotes | Applications | CommissionCode | CommissionPremium | RetainedPremium | ClientResponseID | QuoteResponseID | RUWDaysPending | DWdtmInserted         | DWdtmUpdated         | DWStatusID | Commission | ProductTypeID | SaleDateTimeID       | PremiumWithLoading | BenefitSumInsured | RecommendedBenefitSumInsured | RecommendedRiderCode | NPV_HAS_Comm | ClientPolicyNumber | PolicyStatusID | dtmFirstCollection    | dtmLapseOrCancelDate | PaymentMethodID | PaymentMethod | dtmPaidUpto          | 60DaysDateID | CurrentPremium | dtmDeclaration       | dtmFirstPayment       | ARRA_Statutory | ARRA_Management | PartnerID | MembershipID | ARRA    | ClientBrandID | SaleTimeID | TripTypeID | TripType | StoreStars | SystemID | QuoteDateTimeID      | ConversionPeriod | ProductGroupID | AUDCurrencyRate |
|----------------|------------|-------------|-----------|-------------|-----------|----------|---------|----------------|------------------|-------------------|---------------|-----------------|--------------|-----------|---------------------------|-----------------|------------------|-------|-----------|-------------|--------------------|--------------------|-------------------|--------------------|------------------|--------------------------|-------------------------|------------------|----------------|----------|----------------|--------|---------------|-----------|--------|--------------|----------------|------------------|----------------|-----------------|----------------|----------------|-----------------------|-----------------------|------------|-------------|----------------|-----------------------|-------------------|------------------|---------------------------|-----------------------|--------------|--------------------|----------------|-----------------------|---------------------|-----------------|---------------|---------------------|-------------|----------------|---------------------|---------------------|----------------|----------------|----------|--------------|---------|---------------|------------|------------|----------|------------|----------|---------------------|------------------|----------------|-----------------|
| 1              | 2005-04-27 | 2110000960  | DTH       | FEP         | REMS      | 10003451 | 1       | 2115           | 5                | STP               | 2115          | 5               | -1           | 1         | 1                         | -1              | 0                | 0.000 | NULL      | NULL        | NULL               | NULL               | NULL              | NULL               | NULL             | NULL                     | NULL                    | NULL             | 0              | 0        | 1              | 0      | 205.4400000000 | 0.00      | 0      | 0            |                | 0.000            | NULL           | 9               | 1              | NULL           | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1          | NULL        | 2              | 2005-04-27 00:00:00.000 | 0.000             | 5000.000         | NULL                     | NULL                  | NULL         | 2005-04-27 00:00:00.000 | NULL           | 3                     | Cheque              | NULL            | 2005-06-26 00:00:00.000 | NULL        | 2005-04-27 00:00:00.000 | NULL                | NULL                | NULL           | 0          | NULL         | NULL    | 1             | 00:00:00.0000000 | -1          | Unknown  | NULL    | 1          | 2005-04-27 00:00:00.000 | NULL             | 1              | 1.000000        |
| 1              | 2005-04-27 | 2110000960  | NOR       | FEP         | REMS      | 10003451 | 1       | 2115           | 5                | STP               | 2115          | 5               | -1           | 1         | 1                         | -1              | 0                | 1.000 | 739.0238  | 739.023794121037 | 0                  | 0                 | 0                  | 0                | 0                        | 0                       | 0                | 0              | 1        | 0              | 0      | 0.0000000000   | 5000.00   | 1      | 1            |                | 0.000            | NULL           | 9               | 1              | NULL           | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1          | NULL        | 2              | 2005-04-27 00:00:00.000 | 0.000             | NULL             | NULL                     | 33.6060019556641      | 2110000960  | 60                 | 2005-04-27 00:00:00.000 | 2006-04-26 00:00:00.000 | 3                     | Cheque              | 2006-04-26 00:00:00.000 | 2005-06-26 00:00:00.000 | NULL        | 2005-04-27 00:00:00.000 | NULL                | 682.918771718493 | 608.759953726034 | 0          | NULL         | 682.918771718493 | 1             | 00:00:00.0000000 | -1          | Unknown  | NULL    | 1          | 2005-04-27 00:00:00.000 | 0                | 1              | 1.000000        |
| 1              | 2005-04-27 | 2110000971  | DTH       | FEP         | BDPL      | 10003463 | 1       | 2115           | 5                | STP               | 2115          | 5               | -1           | 1         | 1                         | -1              | 0                | 0.000 | NULL      | NULL        | NULL               | NULL               | NULL              | NULL               | NULL             | NULL                     | NULL                    | NULL             | 0              | 0        | 4              | 0      | 394.8000000000 | 0.00      | 0      | 0            |                | 0.000            | NULL           | 9               | 1              | NULL           | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1          | NULL        | 2              | 2005-04-27 00:00:00.000 | 0.000             | 60000.000        | NULL                     | NULL                  | NULL         | 2005-04-27 00:00:00.000 | NULL           | 2                     | Direct Debit        | NULL            | 2005-06-26 00:00:00.000 | NULL        | 2005-04-27 00:00:00.000 | NULL                | NULL                | NULL           | 0          | NULL         | NULL    | 1             | 00:00:00.0000000 | -1          | Unknown  | NULL    | 1          | 2005-04-27 00:00:00.000 | NULL             | 1              | 1.000000        |
| 1              | 2005-04-27 | 2110000971  | NOR       | FEP         | BDPL      | 10003463 | 1       | 2115           | 5                | STP               | 2115          | 5               | -1           | 1         | 1                         | -1              | 0                | 1.000 | 920.6622  | 920.662212012457 | 0                  | 0                 | 0                  | 0                | 0                        | 0                       | 0                | 0              | 1        | 0              | 0      | 0.0000000000   | 60000.00  | 1      | 1            |                | 0.000            | NULL           | 9               | 1              | NULL           | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1          | NULL        | 2              | 2005-04-27 00:00:00.000 | 0.000             | NULL             | NULL                     | 42.4760065996657      | 2110000971  | 60                 | 2005-04-27 00:00:00.000 | 2008-05-26 00:00:00.000 | 2                     | Direct Debit        | 2008-05-26 00:00:00.000 | 2005-06-26 00:00:00.000 | NULL        | 2005-04-27 00:00:00.000 | NULL                | 851.30701998507  | 758.86275726271  | 0          | NULL         | 851.30701998507  | 1             | 00:00:00.0000000 | -1          | Unknown  | NULL    | 1          | 2005-04-27 00:00:00.000 | 0                | 1              | 1.000000        |
| 1              | 2005-04-27 | 2110000983  | DTH       | FEP         | REMS      | 10003542 | 1       | 2115           | 5                | STP               | 2115          | 5               | -1           | 1         | 1                         | -1              | 0                | 0.000 | NULL      | NULL        | NULL               | NULL               | NULL              | NULL               | NULL             | NULL                     | NULL                    | NULL             | 0              | 0        | 1              | 0      | 171.8400000000 | 0.00      | 0      | 0            |                | 0.000            | NULL           | 9               | 1              | NULL           | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1          | NULL        | 2              | 2005-04-27 00:00:00.000 | 0.000             | 5000.000         | NULL                     | NULL                  | NULL         | 2005-04-27 00:00:00.000 | NULL           | 2                     | Direct Debit        | NULL            | 2005-06-26 00:00:00.000 | NULL        | 2005-04-27 00:00:00.000 | NULL                | NULL                | NULL           | 0          | NULL         | NULL    | 1             | 00:00:00.0000000 | -1          | Unknown  | NULL    | 1          | 2005-04-27 00:00:00.000 | NULL             | 1              | 1.000000        |
| 1              | 2005-04-27 | 2110000983  | NOR       | FEP         | REMS      | 10003542 | 1       | 2115           | 5                | STP               | 2115          | 5               | -1           | 1         | 1                         | -1              | 0                | 1.000 | 551.4398  | 551.439803248217 | 0                  | 0                 | 0                  | 0                | 0                        | 0                       | 0                | 0              | 1        | 0              | 0      | 0.0000000000   | 5000.00   | 1      | 1            |                | 0.000            | NULL           | 9               | 1              | NULL           | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1          | NULL        | 2              | 2005-04-27 00:00:00.000 | 0.000             | NULL             | NULL                     | 25.4414272862246      | 2110000983  | 60                 | 2005-04-27 00:00:00.000 | 2005-05-26 00:00:00.000 | 2                     | Direct Debit        | 2005-05-26 00:00:00.000 | 2005-06-26 00:00:00.000 | NULL        | 2005-04-27 00:00:00.000 | NULL                | 509.898820087601 | 454.528408027771 | 0          | NULL         | 509.898820087601 | 1             | 00:00:00.0000000 | -1          | Unknown  | NULL    | 1          | 2005-04-27 00:00:00.000 | 0                | 1              | 1.000000        |


##  1. Data Overview & Sanity Checks

```sql
-- Total number of rows
SELECT COUNT(*) AS TotalRecords FROM dbo.FactSalesActivity;
TotalRecords
18519027

-- Distinct values per key column
SELECT COUNT(DISTINCT QuoteID) AS UniqueQuotes, COUNT(DISTINCT ClientID) AS UniqueClients FROM dbo.FactSalesActivity;
UniqueQuotes	UniqueClients
10183589	7445054

-- Number of records per Source System
SELECT SourceSystemID, COUNT(*) AS RecordCount FROM dbo.FactSalesActivity GROUP BY SourceSystemID;
SourceSystemID	RecordCount
1	16568233
2	1950794
```

### Key Insights - Data Volume and Scope
The FactSalesActivity table contains over 18.5 million records representing sales activities. The data primarily comes from two source systems, with source system ID 1 contributing 89.5% of the records (16.57 million) and source system ID 2 providing the remaining 10.5% (1.95 million). The table contains approximately 10.2 million unique quotes associated with 7.4 million unique clients, showing that some clients have multiple quotes and potentially multiple policies. This indicates a significant customer base with repeat business or multiple product holdings being captured in the system.

----------

##  2. Sales Insights

```sql
-- Total Sales and Premium
SELECT SUM(Sales) AS TotalSales, SUM(Premium) AS TotalPremium FROM dbo.FactSalesActivity;
TotalSales	TotalPremium
2017085	2027604778.343

-- Total Lives Sold and Actual Lives Sold
SELECT SUM(LivesSold) AS TotalLivesSold, SUM(LivesSold_Actual) AS TotalLivesSold_Actual FROM dbo.FactSalesActivity;
TotalLivesSold	TotalLivesSold_Actual
1772513	1873721

-- Sales by Brand
SELECT BrandID, SUM(Sales) AS TotalSales FROM dbo.FactSalesActivity GROUP BY BrandID ORDER BY TotalSales DESC;
BrandID	TotalSales
2	601875
1	578407
9	484695
3	94046
1001	49746
7	39444
11	36294
17	28378
16	27035
13	21880
4	14285
5	13837
18	12914
10	9131
15	3346
14	1147
12	625

-- Top ProductCodes by Total Premium
SELECT ProductTypeID, SUM(Premium) AS TotalPremium FROM dbo.FactSalesActivity GROUP BY ProductTypeID ORDER BY TotalPremium DESC;
ProductTypeID	TotalPremium
3	511632168.818
1	498775042.979
2	394355910.576
7	147508695.540
6	141479249.500
9	129581165.430
4	118554738.980
8	38834186.250
12	37266735.640
10	9616884.630
```

### Key Insights - Sales Performance
The table records over 2 million total successful sales (2,017,085) generating more than $2 billion in premiums. The difference between LivesSold (1,772,513) and LivesSold_Actual (1,873,721) suggests that there's approximately 5.7% variance in how lives covered are being reported versus the actual lives covered, which could indicate reporting inconsistencies or special policy cases.

Brand performance analysis reveals that three brands dominate sales volume, with BrandIDs 2, 1, and 9 collectively accounting for 82.6% of total sales. This indicates strong market concentration among the top brands. The top three product types (IDs 3, 1, and 2) generate the majority of premium revenue ($1.4 billion), representing 69.3% of the total premium income. This suggests that the business strategy should focus on these key product types and brands for optimal growth.

----------

## 3. Commission & NPV Insights

```sql
-- Total Commissions
SELECT SUM(Commission) AS TotalCommission FROM dbo.FactSalesActivity;
TotalCommission
55530770.435

-- Total NPV values by type
SELECT 
    SUM(NPV_Gross_HFS_Comm) AS GrossHFS,
    SUM(NPV_Insurer_Upfront) AS InsurerUpfront,
    SUM(NPV_Partner_Upfront) AS PartnerUpfront,
    SUM(NPV_SalesIncentive_Upfront) AS SalesIncentiveUpfront
FROM dbo.FactSalesActivity;
GrossHFS	InsurerUpfront	PartnerUpfront	SalesIncentiveUpfront
3150914018.71582	2484197.58576188	0	6492941.77728279

-- Real Liability vs Actual Premium
SELECT SUM(NPV_RealLiability) AS TotalLiability, SUM(Premium) AS TotalPremium FROM dbo.FactSalesActivity;
TotalLiability	TotalPremium
54790527.5235554	2027604778.343
```

### Key Insights - Financial Performance and Profitability
Commission data reveals total commissions of approximately $55.5 million against premium revenue of $2.03 billion, representing an overall commission rate of about 2.7%. This relatively low rate may indicate either a direct sales model or competitive pricing strategy to gain market share.

The Net Present Value (NPV) calculations reveal important financial metrics. The NPV_Gross_HFS_Comm of $3.15 billion significantly exceeds the total premium collected, showing the long-term value of the policies beyond the immediate premium income. This represents the time value of expected future commission streams, suggesting a healthy long-term business model.

The disparity between NPV_RealLiability ($54.8 million) and total premium ($2.03 billion) indicates that the company maintains a favorable ratio of liabilities to premium income (only about 2.7% of premium value), which suggests effective risk management practices. The negligible NPV_Partner_Upfront value (0) contrasted with significant NPV_Insurer_Upfront ($2.48 million) and NPV_SalesIncentive_Upfront ($6.49 million) indicates that the sales model prioritizes direct incentives to sales staff rather than partner commissions.

----------

## 4. Policy and Payment Behavior

```sql
-- Active vs Lapsed/Cancelled Policies
SELECT PolicyStatusID, COUNT(*) AS PolicyCount FROM dbo.FactSalesActivity GROUP BY PolicyStatusID;
PolicyStatusID	PolicyCount
NULL	17154791
20	1212
30	543337
40	7752
50	124085
60	655116
61	32608
70	126

-- Distribution of Payment Methods
SELECT PaymentMethod, COUNT(*) AS Count FROM dbo.FactSalesActivity GROUP BY PaymentMethod;
PaymentMethod	Count
NULL	13881686
Cheque	13393
Credit Card	1791104
Direct Debit	2832844

-- Collection Delay Analysis
SELECT AVG(CollectionDelay) AS AvgCollectionDelay, MAX(CollectionDelay) AS MaxDelay FROM dbo.FactSalesActivity;
AvgCollectionDelay	MaxDelay
0	482
```

### Key Insights - Policy Status and Payment Patterns
The majority of records (92.6%) have a NULL PolicyStatusID, which may indicate either records that represent quotes and applications rather than active policies, or incomplete data capture. Among records with defined status, policies with status 60 (655,116) and 30 (543,337) are the most common, representing approximately 86.4% of all policies with a defined status. These likely represent active and lapsed policies respectively.

Payment method analysis shows that Direct Debit is the most common specified payment method (61.1% of specified methods), followed by Credit Card (38.6%). The prevalence of Direct Debit suggests a focus on recurring payment convenience and potentially better collection rates. The minimal use of Cheque payments (0.3% of specified methods) reflects the industry-wide trend away from paper-based payment methods.

The average collection delay of 0 days suggests efficient payment processing overall, but the maximum delay of 482 days indicates significant outliers requiring attention for collections management. The presence of such extreme delays may warrant a review of collection procedures and risk assessment for certain customer segments.

----------

## 5. Product and Channel Performance

```sql
-- Product performance by Group
SELECT ProductGroupID, SUM(Premium) AS TotalPremium FROM dbo.FactSalesActivity GROUP BY ProductGroupID ORDER BY TotalPremium DESC;
ProductGroupID	TotalPremium
1	1048952428.175
3	511632168.818
4	147508695.540
2	141479249.500
7	129581165.430
6	38834186.250
8	9616884.630

-- Channel-wise Sales
SELECT ChannelID, SUM(Sales) AS TotalSales FROM dbo.FactSalesActivity GROUP BY ChannelID ORDER BY TotalSales DESC;
ChannelID	TotalSales
1	1786569
2	230516
```

### Key Insights - Product Mix and Distribution Strategy
Product Group 1 dominates premium generation with over $1.04 billion in premiums, accounting for 51.7% of total premium income. This is followed by Product Group 3 with $511.6 million (25.2%). Together, these two product groups generate 77% of premium revenue, highlighting areas of business strength and potential concentration risk.

Sales channel analysis reveals that Channel 1 is responsible for 88.6% of total sales (1,786,569 units), making it the primary distribution channel. Channel 2, with 11.4% of sales (230,516 units), represents a secondary but still significant channel. This heavy reliance on a single channel suggests both a strength in that channel's effectiveness but also a potential strategic vulnerability if that channel were to be disrupted.

----------

## 6. Member/Partner Behavior

```sql
-- Sales split by Medibank Membership
SELECT IsMedibankMember, COUNT(*) AS Count, SUM(Sales) AS Sales FROM dbo.FactSalesActivity GROUP BY IsMedibankMember;
IsMedibankMember	Count	Sales
0	16929511	1904538
1	1589516	112547

-- Sales by Partner
SELECT PartnerID, SUM(Sales) AS TotalSales FROM dbo.FactSalesActivity GROUP BY PartnerID ORDER BY TotalSales DESC;
PartnerID	TotalSales
0	1808054
1	181388
2	14286
3	13357
```

### Key Insights - Strategic Partnerships
Only 8.6% of records are associated with Medibank members, but these contribute to 5.6% of total sales (112,547 units). This suggests that while the Medibank partnership provides additional sales, non-Medibank customers remain the primary business source. The conversion rate from records to sales is slightly lower for Medibank members (7.1% vs. 11.2% for non-members), which might indicate differences in sales approach or product alignment for this segment.

Partner analysis reveals that Partner ID 0 (likely direct sales or no partner attribution) accounts for 89.7% of sales (1,808,054 units). Partner ID 1 contributes 9.0% of sales, while Partners 2 and 3 collectively add just 1.4%. This underscores the company's reliance on direct sales channels or primary partnership, with minimal diversification across multiple partners. This concentration in distribution strategy could be both a strength in terms of operational focus and a risk in terms of dependency.

----------

## 7. Conversion & Application Funnel

```sql
-- Conversion ratio: Quotes → Applications → Sales
SELECT 
    SUM(Quotes) AS TotalQuotes,
    SUM(Applications) AS TotalApplications,
    SUM(Sales) AS TotalSales,
    ROUND(SUM(Applications) * 1.0 / NULLIF(SUM(Quotes), 0), 2) AS ApplicationRate,
    ROUND(SUM(Sales) * 1.0 / NULLIF(SUM(Applications), 0), 2) AS SalesConversionRate
FROM dbo.FactSalesActivity;
TotalQuotes	TotalApplications	TotalSales	ApplicationRate	SalesConversionRate
15563623	8647474	2017085	0.56	0.23
```

### Key Insights - Sales Funnel Efficiency
The sales funnel metrics reveal a structured conversion process with defined stages. 56% of quotes progress to application stage, indicating a reasonably effective initial engagement process. However, only 23% of applications convert to actual sales, resulting in an end-to-end quote-to-sale conversion rate of just 13%. 

This highlights significant drop-off at both major conversion points. The larger drop in the application-to-sale stage (77% loss) compared to quote-to-application stage (44% loss) suggests that qualifying prospects earlier in the process or improving the application experience could yield better efficiency. These conversion metrics provide clear targets for sales process optimization and customer journey improvements.

----------

## 8. Time-Related Insights

```sql
-- Earliest and Latest Sale Dates
SELECT MIN(SaleDateTimeID) AS EarliestSaleDateID, MAX(SaleDateTimeID) AS LatestSaleDateID FROM dbo.FactSalesActivity;
EarliestSaleDateID	LatestSaleDateID
2005-04-27 00:00:00.000	Yesterday 00:30:00

-- Premium Over Time Buckets (Not month-by-month)
SELECT 
    CASE 
        WHEN YEAR(SaleDateTimeID) = 2022 THEN '2022'
        WHEN YEAR(SaleDateTimeID) = 2023 THEN '2023'
        ELSE 'Other'
    END AS SaleYear,
    SUM(Premium) AS TotalPremium
FROM dbo.FactSalesActivity
GROUP BY 
    CASE 
        WHEN YEAR(SaleDateTimeID) = 2022 THEN '2022'
        WHEN YEAR(SaleDateTimeID) = 2023 THEN '2023'
        ELSE 'Other'
    END;
SaleYear	TotalPremium
2022	132846625.990
2023	154812495.220
Other	1739945657.133
```

### Key Insights - Temporal Trends and Seasonality
The data spans from April 27, 2005, to the present day, representing nearly 20 years of sales activities. This long-term dataset enables robust historical analysis and trend identification. Recent years show significant premium generation with 2023 ($154.8 million) showing a 16.5% increase over 2022 ($132.8 million), indicating positive business growth momentum in the recent period.

The majority of premium value ($1.74 billion or 85.8%) comes from years other than 2022-2023, reflecting the long-term nature of the insurance business where policies sold in previous years continue to provide premium income. This highlights the importance of customer retention and policy renewal strategies for the overall financial health of the business.

----------

## 9. Data Quality Checks

```sql
-- Null checks for important columns
SELECT 
    SUM(CASE WHEN QuoteID IS NULL THEN 1 ELSE 0 END) AS NullQuoteID,
    SUM(CASE WHEN Premium IS NULL THEN 1 ELSE 0 END) AS NullPremium,
    SUM(CASE WHEN SaleDateTimeID IS NULL THEN 1 ELSE 0 END) AS NullSaleDateTime
FROM dbo.FactSalesActivity;
NullQuoteID	NullPremium	NullSaleDateTime
0	1819	13563815

-- Count of negative premium values
SELECT COUNT(*) AS NegativePremiumCount FROM dbo.FactSalesActivity WHERE Premium < 0;
NegativePremiumCount
93
```

### Key Insights - Data Quality Assessment
Data quality analysis reveals several important findings. QuoteID shows strong data integrity with zero null values, establishing it as a reliable unique identifier for records. However, Premium values contain 1,819 null records (0.01% of total), which may represent quotes or applications rather than completed sales, or could be data entry issues requiring attention.

A significant concern is that 73.2% of records (13,563,815) are missing SaleDateTimeID values. This suggests that these records might represent quotes or applications rather than completed sales, or it could indicate systematic data capture issues in the sales process. 

The presence of 93 negative premium values is a data quality issue that warrants investigation, as premium amounts should typically be positive. These may represent adjustments, refunds, or data entry errors. While small in number, these records could impact aggregate financial calculations if not properly accounted for in reporting.

----------

## 10. Business Performance and Strategy Implications

### Market Positioning and Product Strategy
The data reveals a strong market position with over $2 billion in premium revenue across multiple product lines and brands. The concentration of revenue in specific product types (especially Product Type IDs 3, 1, and 2) suggests areas of competitive advantage. Strategic product development should focus on these strengths while exploring diversification opportunities in emerging segments.

### Distribution Channel Optimization
The heavy reliance on Channel 1 (88.6% of sales) presents both an opportunity and a risk. While this channel clearly performs well, the dependency creates vulnerability. Investment in developing Channel 2 and exploring new channels could provide more balanced growth opportunities and risk mitigation.

### Financial Management and Profitability
The significant difference between NPV calculations and current premium income indicates a business model built on long-term value rather than short-term revenue. With NPV_Gross_HFS_Comm at $3.15 billion versus current premium of $2.03 billion, the company is effectively capturing future value streams. This supports continued investment in customer acquisition despite the relatively modest 13% quote-to-sale conversion rate.

### Sales Process Efficiency
The sales funnel analysis highlights opportunities for process improvement, particularly at the application-to-sale stage where 77% of applications fail to convert. Targeted interventions at this stage, such as streamlining underwriting, improving communication, or enhancing sales training, could significantly impact overall business performance.

### Customer Retention and Policy Management
The policy status distribution indicates areas for retention improvement. With significant numbers of policies in status categories that likely represent non-active states (status 30, 50), there's opportunity to develop targeted retention strategies. The excellent collection efficiency (average delay of 0 days) suggests strong operational processes that could be leveraged for improved customer experience and retention.

### Strategic Partnerships
While Medibank members represent a modest portion of sales (5.6%), this partnership likely remains valuable for brand association and customer acquisition. Evaluation of the partnership's efficiency and exploration of similar arrangements could provide growth opportunities without significant capital investment.


