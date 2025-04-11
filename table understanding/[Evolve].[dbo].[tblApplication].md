# [Evolve].[dbo].[tblApplication]

```sql
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [ApplicationId]
      ,[QuoteId]
      ,[ClientId]
      ,[JointClientId]
      ,[dtmInserted]
      ,[dtmAppInserted]
      ,[CreatedBy]
      ,[AppStatusId]
      ,[RuwStatusId]
      ,[dtmReferred]
      ,[OccupationId]
      ,[JointOccupationId]
      ,[OccupationClass]
      ,[OccupationClassId]
      ,[JointOccupationClassId]
      ,[JointRelationId]
      ,[Income]
      ,[EmploymentTypeId]
      ,[dtmDeclaration]
      ,[dtmRUWClosed]
      ,[RuwClosedBy]
      ,[IsInitialApplication]
      ,[DutyBasedAssessmentId]
  FROM [Evolve].[dbo].[tblApplication]
```

## Sample Data

| ApplicationId | QuoteId   | ClientId | JointClientId | dtmInserted         | dtmAppInserted      | CreatedBy | AppStatusId | RuwStatusId | dtmReferred | OccupationId | JointOccupationId | OccupationClass | OccupationClassId | JointOccupationClassId | JointRelationId | Income | EmploymentTypeId | dtmDeclaration | dtmRUWClosed | RuwClosedBy | IsInitialApplication | DutyBasedAssessmentId |
|---------------|-----------|----------|---------------|---------------------|---------------------|-----------|-------------|-------------|-------------|--------------|-------------------|-----------------|-------------------|-----------------------|----------------|-------|-----------------|----------------|-------------|------------|---------------------|-----------------------|
| 12199108      | 12163808  | 1        | 22926740      | 2020-01-29 11:19:00 | 2020-01-29 11:22:00 | KapilJ01  | 2           | NULL        | NULL        | NULL         | NULL              | NULL            | NULL              | NULL                  | 5              | 0     | NULL            | NULL           | NULL        | NULL       | 1                   | NULL                  |
| 12401326      | 12364830  | 1        | 23188125      | 2020-05-25 15:26:00 | 2020-05-25 15:40:00 | KapilJ01  | 6           | NULL        | NULL        | NULL         | NULL              | NULL            | NULL              | NULL                  | 15             | 0     | NULL            | NULL           | NULL        | NULL       | 1                   | NULL                  |
| 12530428      | 12492748  | 1        | NULL          | 2020-07-29 10:57:00 | 2020-07-29 10:57:00 | FredeK01  | 2           | NULL        | NULL        | NULL         | NULL              | NULL            | NULL              | NULL                  | NULL           | 0     | NULL            | NULL           | NULL        | NULL       | 1                   | NULL                  |
| 12530447      | 12492767  | 1        | NULL          | 2020-07-29 11:02:00 | 2020-07-29 11:04:00 | FredeK01  | 2           | NULL        | NULL        | NULL         | NULL              | NULL            | NULL              | NULL                  | NULL           | 0     | NULL            | NULL           | NULL        | NULL       | 1                   | NULL                  |
| 12530453      | 12492773  | 1        | NULL          | 2020-07-29 11:05:00 | 2020-07-29 11:07:00 | FredeK01  | 6           | NULL        | NULL        | NULL         | NULL              | NULL            | NULL              | NULL                  | NULL           | 0     | NULL            | NULL           | NULL        | NULL       | 1                   | NULL                  |
| 12530481      | 12492798  | 1        | NULL          | 2020-07-29 11:12:00 | 2020-07-29 11:12:00 | FredeK01  | 2           | NULL        | NULL        | NULL         | NULL              | NULL            | NULL              | NULL                  | NULL           | 0     | NULL            | NULL           | NULL        | NULL       | 1                   | NULL                  |


## 1. General Data Profiling
```sql
-- Total number of applications
SELECT COUNT(*) AS TotalApplications FROM [Evolve].[dbo].[tblApplication];
TotalApplications
13553569

-- Number of distinct clients
SELECT COUNT(DISTINCT ClientId) AS DistinctClients FROM [Evolve].[dbo].[tblApplication];
DistinctClients
4305899

-- Number of joint applications
SELECT COUNT(*) AS JointApplications FROM [Evolve].[dbo].[tblApplication] WHERE JointClientId IS NOT NULL;
JointApplications
1108521

-- Count of initial vs. non-initial applications
SELECT IsInitialApplication, COUNT(*) AS Count FROM [Evolve].[dbo].[tblApplication] GROUP BY IsInitialApplication;
IsInitialApplication	Count
0	488382
1	13065187
```

----------

## 2. Time-Based Insights
```sql
-- Applications inserted each year
SELECT YEAR(dtmInserted) AS Year, COUNT(*) AS ApplicationCount 
FROM [Evolve].[dbo].[tblApplication] 
GROUP BY YEAR(dtmInserted) 
ORDER BY Year;
Year	ApplicationCount
2005	1030
2006	1458
2007	2259
2008	110926
2009	414482
2010	647854
2011	753355
2012	779844
2013	637564
2014	571368
2015	572108
2016	620986
2017	1050602
2018	1883772
2019	2391567
2020	721246
2021	671816
2022	646334
2023	523904
2024	412061
2025	139033

-- Count of applications with missing dtmInserted or dtmAppInserted
SELECT 
  SUM(CASE WHEN dtmInserted IS NULL THEN 1 ELSE 0 END) AS Missing_dtmInserted,
  SUM(CASE WHEN dtmAppInserted IS NULL THEN 1 ELSE 0 END) AS Missing_dtmAppInserted
FROM [Evolve].[dbo].[tblApplication];
Missing_dtmInserted	Missing_dtmAppInserted
0	10093627
```

----------

## 3. Employment and Occupation
```sql
-- Top 10 most frequent occupations (based on OccupationId)
SELECT TOP 10 OccupationId, COUNT(*) AS Count 
FROM [Evolve].[dbo].[tblApplication] 
GROUP BY OccupationId 
ORDER BY Count DESC;
OccupationId	Count
NULL	11024869
0	1685349
33	23517
31	19951
21	17441
195	14873
648	13257
920	13033
973	12664
32	11877

-- Employment types with most applications
SELECT EmploymentTypeId, COUNT(*) AS Count 
FROM [Evolve].[dbo].[tblApplication] 
GROUP BY EmploymentTypeId 
ORDER BY Count DESC;
EmploymentTypeId	Count
NULL	12855301
2	661722
1	36546

-- Applications by Occupation Class
SELECT OccupationClass, COUNT(*) AS Count 
FROM [Evolve].[dbo].[tblApplication] 
GROUP BY OccupationClass 
ORDER BY Count DESC;
OccupationClass	Count
NULL	12266165
	644623
C	225716
A	199542
B	103723
E	45485
F	33589
G	29335
H	2878
D	1523
I	990
```

----------

## 4. Status Analysis
```sql
-- Most common application statuses
SELECT AppStatusId, COUNT(*) AS Count 
FROM [Evolve].[dbo].[tblApplication] 
GROUP BY AppStatusId 
ORDER BY Count DESC;
AppStatusId	Count
2	11862859
3	1047440
15	402875
6	191650
0	26457
10	15727
7	2702
1	1380
12	954
8	688
11	330
13	238
5	147
9	59
14	27
4	24
NULL	12

-- Most common underwriting statuses
SELECT RuwStatusId, COUNT(*) AS Count 
FROM [Evolve].[dbo].[tblApplication] 
GROUP BY RuwStatusId 
ORDER BY Count DESC;
RuwStatusId	Count
NULL	13401236
5	115216
4	30282
1	3740
3	2994
2	92
0	9

-- Applications that were referred
SELECT COUNT(*) AS ReferredApplications 
FROM [Evolve].[dbo].[tblApplication] 
WHERE dtmReferred IS NOT NULL;
ReferredApplications
143635

-- Applications that were referred but not closed
SELECT COUNT(*) AS ReferredNotClosed 
FROM [Evolve].[dbo].[tblApplication] 
WHERE dtmReferred IS NOT NULL AND dtmRUWClosed IS NULL;
ReferredNotClosed
28474
```

----------

## 5. Income & Assessment
```sql
-- Average income across applications
SELECT AVG(CAST(Income AS DECIMAL(18,2))) AS AvgIncome
FROM [Evolve].[dbo].[tblApplication]
WHERE Income IS NOT NULL;
AvgIncome
1851.338369
```

----------

## 6. User Activity
```sql
-- Top 10 creators of applications
SELECT TOP 10 CreatedBy, COUNT(*) AS CreatedCount 
FROM [Evolve].[dbo].[tblApplication] 
GROUP BY CreatedBy 
ORDER BY CreatedCount DESC;
CreatedBy	CreatedCount
OnlineUser	6879821
HeidiP01	43106
KapilJ01	42847
YoussH01	41486
HowadH01	40557
perosl01	40082
bronwh01	38743
ireneh01	38094
sophih01	36431
AlfreA01	36428

-- Top 10 users who closed the RUW process
SELECT TOP 10 RuwClosedBy, COUNT(*) AS ClosedCount 
FROM [Evolve].[dbo].[tblApplication] 
WHERE RuwClosedBy IS NOT NULL 
GROUP BY RuwClosedBy 
ORDER BY ClosedCount DESC;
RuwClosedBy	ClosedCount
KevinP01	949
bronwh01	847
KapilJ01	813
RitaB01	779
joseps01	770
zinal01	710
ireneh01	701
melink01	683
JoelH01	667
RoberA02	642
```

----------

## 7. Data Completeness & Anomalies
```sql
-- Count of rows where essential IDs are missing
SELECT 
  SUM(CASE WHEN QuoteId IS NULL THEN 1 ELSE 0 END) AS MissingQuoteId,
  SUM(CASE WHEN ClientId IS NULL THEN 1 ELSE 0 END) AS MissingClientId,
  SUM(CASE WHEN ApplicationId IS NULL THEN 1 ELSE 0 END) AS MissingApplicationId
FROM [Evolve].[dbo].[tblApplication];
MissingQuoteId	MissingClientId	MissingApplicationId
0	0	0

-- Applications with missing both OccupationId and OccupationClass
SELECT COUNT(*) AS MissingOccupationData 
FROM [Evolve].[dbo].[tblApplication] 
WHERE OccupationId IS NULL AND OccupationClass IS NULL;
MissingOccupationData
10737539
```

----------

## 8. Column Descriptions

| Column Name | Data Type | Description | Key Information |
|-------------|-----------|-------------|----------------|
| ApplicationId | Integer | Primary key identifier for each application record | No missing values; uniquely identifies each application |
| QuoteId | Integer | Foreign key linking to the quote record associated with this application | No missing values; vital for tracking application origin |
| ClientId | Integer | Foreign key linking to the main client/applicant | No missing values; represents the primary applicant |
| JointClientId | Integer | Foreign key linking to a secondary applicant if applicable | Present in 1,108,521 records (8.2% of applications); indicates joint applications |
| dtmInserted | Datetime | Timestamp when record was inserted into database | No missing values; allows tracking of record creation |
| dtmAppInserted | Datetime | Timestamp when application was officially inserted | Missing in 10,093,627 records (74.5%); represents formal application submission time |
| CreatedBy | Varchar | User ID or username of person who created the application | "OnlineUser" accounts for 6,879,821 records (50.8%); helps track application source |
| AppStatusId | Integer | Status code of the application | Most common values: 2 (87.5%), 3 (7.7%), 15 (3.0%); critical for workflow status tracking |
| RuwStatusId | Integer | Risk underwriting status code | Null in 13,401,236 records (98.9%); value 5 in 115,216 records (0.9%) |
| dtmReferred | Datetime | Timestamp when application was referred for review | Present in 143,635 records (1.1%); indicates special handling requirements |
| OccupationId | Integer | Foreign key to occupation reference table | Null in 11,024,869 records (81.3%); value 0 in 1,685,349 records (12.4%) |
| JointOccupationId | Integer | Foreign key to occupation for joint applicant | Sparsely populated; used only for joint applications |
| OccupationClass | Varchar | Classification code for occupation risk assessment | Null in 12,266,165 records (90.5%); values A-I represent risk categories |
| OccupationClassId | Integer | ID reference for occupation class | Sparsely populated; formal reference to occupation class codes |
| JointOccupationClassId | Integer | ID for joint applicant's occupation class | Sparsely populated; relevant only for joint applications |
| JointRelationId | Integer | Code indicating relationship between applicants | Values 5 and 15 are most common; relevant only for joint applications |
| Income | Decimal | Reported income of applicant | Average value of 1,851.34 for non-null records; often zero or null |
| EmploymentTypeId | Integer | Code for type of employment | Null in 12,855,301 records (94.8%); value 2 in 661,722 records (4.9%) |
| dtmDeclaration | Datetime | Timestamp when declaration was submitted | Sparsely populated; represents when applicant formally declared information |
| dtmRUWClosed | Datetime | Timestamp when risk underwriting was closed | Present when underwriting process completed; linked to RuwClosedBy |
| RuwClosedBy | Varchar | User who closed the risk underwriting process | KevinP01 is top closer (949 records); significant for accountability in underwriting |
| IsInitialApplication | Bit | Flag indicating if this is the first application (1) or a subsequent one (0) | 1 in 13,065,187 records (96.4%); 0 in 488,382 records (3.6%) |
| DutyBasedAssessmentId | Integer | ID reference for duty-based assessment | Sparsely populated; used for regulatory compliance assessments |

## 9. Key Insights Summary

### Application Overview
- **Volume**: The database contains 13,553,569 application records spanning from 2005 to 2025.
- **Growth Pattern**: Application volume grew steadily from 2005 to 2019, with peak volume in 2019 (2,391,567 applications), followed by a decline through 2020-2025.
- **Client Base**: 4,305,899 distinct clients have applications in the system, with some clients having multiple applications.
- **Joint Applications**: 8.2% of applications (1,108,521) are joint applications involving two clients.
- **Application Type**: 96.4% are flagged as initial applications, suggesting most clients don't submit multiple applications.

### Application Workflow
- **Status Distribution**: The vast majority of applications (87.5%) have AppStatusId=2, likely representing a standard processing state.
- **Referral Processing**: 143,635 applications (1.1%) were referred for special review, with 28,474 (19.8% of referrals) still not closed.
- **Underwriting**: Only 1.1% of applications have a non-null RuwStatusId, indicating most applications don't require detailed underwriting.
- **User Activity**: System user "OnlineUser" created 50.8% of all applications, suggesting heavy reliance on self-service channels.
- **Staff Processing**: Among human users, HeidiP01, KapilJ01, and YoussH01 are the top application creators, each handling over 40,000 applications.

### Data Quality Concerns
- **Missing Data**: Critical ID fields (ApplicationId, QuoteId, ClientId) have no missing values, ensuring data integrity for key identifiers.
- **Incomplete Records**: Occupation data is missing in 79.2% of records (10,737,539 applications have neither OccupationId nor OccupationClass).
- **Timestamp Gaps**: While dtmInserted is complete for all records, dtmAppInserted is missing in 74.5% of records.
- **Employment Information**: Employment type is missing for 94.8% of applications, limiting analysis of applicant employment profiles.
- **Income Reporting**: Income data shows an average of 1,851.34, but has many zero or null values, suggesting inconsistent reporting.

### Operational Insights
- **Seasonal Patterns**: [Analysis of application volume by month or day of week would provide additional seasonal insights]
- **Processing Efficiency**: The time difference between dtmInserted and dtmAppInserted (when both are available) indicates application processing speed.
- **Underwriting Workload**: Specific users (KevinP01, bronwh01, KapilJ01) handle a disproportionate share of underwriting closures.
- **Online vs. Agent Applications**: The high proportion of "OnlineUser" creations indicates significant online self-service adoption.

### Business Recommendations
- **Data Quality**: Improve collection of occupation and employment data, which is missing in over 79% of applications.
- **Process Optimization**: Address the 28,474 applications that were referred but never closed to reduce processing backlogs.
- **User Training**: Analyze the practices of top-performing users (by volume and completion rate) to identify best practices.
- **Trend Analysis**: Investigate the decline in application volume since 2019 to understand market or competitive changes.
- **Joint Application Process**: Review the joint application process, which represents only 8.2% of applications despite potential market opportunity.

----------




