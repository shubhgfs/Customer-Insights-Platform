# [HollardDW].[dbo].[DimClient]

```sql
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [SourceSystemID]
      ,[ClientID]
      ,[ProductSetID]
      ,[ClientRowNum]
      ,[Title]
      ,[DOB]
      ,[FirstName]
      ,[SecondName]
      ,[Surname]
      ,[Gender]
      ,[PhoneH]
      ,[PhoneM]
      ,[IsResidentOfBrandCountryId]
      ,[Email]
      ,[CreationDateID]
      ,[CreationDate]
      ,[CreatedBy]
      ,[BrandID]
      ,[BrandName]
      ,[IsLead]
      ,[AllocatedUserID]
      ,[StatusID]
      ,[AddressLine1]
      ,[Suburb]
      ,[State]
      ,[PostCode]
      ,[CampaignBatchID]
      ,[PostalAddressLine1]
      ,[PostalSuburb]
      ,[PostalState]
      ,[PostalPostcode]
      ,[dtmLastUpdated]
      ,[SourceID]
      ,[IsDeleted]
      ,[CentrixID]
      ,[IsNewCentrixClient]
      ,[ClientStatusID]
      ,[IsInbound]
      ,[WorkItemID]
      ,[WorkItem]
      ,[GNCStepDesc]
      ,[dtmOutbound]
      ,[dtmFirstContact]
      ,[ClientLeadAllocatedUserID]
      ,[dtmFirstContactDateID]
      ,[dtmNextCallBack]
      ,[DWdtmInserted]
      ,[DWdtmUpdated]
      ,[DWStatusID]
      ,[ClientLeadWorkItemID]
      ,[PartnerID]
      ,[IsMedibankMember]
      ,[MembershipID]
      ,[SystemID]
      ,[ClientLeadSourceID]
      ,[OriginalPartnerID]
  FROM [HollardDW].[dbo].[DimClient]
```

## Sample Data

| SourceSystemID | ClientID | ProductSetID | ClientRowNum | Title | DOB | FirstName | SecondName | Surname | Gender | PhoneH | PhoneM | IsResidentOfBrandCountryId | Email | CreationDateID | CreationDate | CreatedBy | BrandID | BrandName | IsLead | AllocatedUserID | StatusID | AddressLine1 | Suburb | State | PostCode | CampaignBatchID | PostalAddressLine1 | PostalSuburb | PostalState | PostalPostcode | dtmLastUpdated | SourceID | IsDeleted | CentrixID | IsNewCentrixClient | ClientStatusID | IsInbound | WorkItemID | WorkItem | GNCStepDesc | dtmOutbound | dtmFirstContact | ClientLeadAllocatedUserID | dtmFirstContactDateID | dtmNextCallBack | DWdtmInserted | DWdtmUpdated | DWStatusID | ClientLeadWorkItemID | PartnerID | IsMedibankMember | MembershipID | SystemID | ClientLeadSourceID | OriginalPartnerID |
|----------------|----------|--------------|--------------|-------|-----|-----------|------------|---------|--------|--------|--------|---------------------------|-------|-----------------|--------------|----------|---------|-----------|--------|-----------------|----------|--------------|--------|-------|----------|------------------|-------------------|--------------|-------------|-----------------|----------------|----------|-----------|----------|-------------------|----------------|----------|------------|----------|-------------|-------------|----------------|------------------------|-----------------------|-----------------|----------------|--------------|------------|--------------------|-----------|-------------------|--------------|----------|--------------------|--------------------|
| 1              | 3000000  | -1           | 1            | NULL  | 1953-02-20 00:00:00 | DAVID JOHN | NULL       | WILSON  | Male   | NULL   | NULL   | 1                         | NA    | 2007-01-05 00:00:00 | 2007-01-05 18:11:00 | ibrahq01 | 1       | Real      | 1      | caterc01         | 4        | NULL         | NULL   | NULL  | NULL     | NULL             | NULL              | NULL         | NULL        | NULL            | 2022-01-12 23:24:00 | 98      | 0         | NULL     | NULL              | -1              | 1        | 10          | Inbound Call - New Lead | Inbound Call - New Lead | NULL         | 2007-01-05 18:11:00.000 | caterc01   | 2007-01-05 00:00:00.000 | NULL       | 2025-04-09 00:00:00.000 | 2025-04-09 00:00:00.000 | 1        | 10              | 0        | 0        | NULL              | 1                  | 98         | 0       |
| 2              | 3000000  | -1           | 1            | Mr    | 1962-06-19 00:00:00 | Tony      | NULL       | Buxton  | Male   | 0412178948 | NULL | 1                         | flansley@avenir.net.au | 2011-08-10 00:00:00 | 2011-08-10 12:24:00 | dakshS01 | -1      | Unknown   | 1      | samues01         | 4        | 1 Fairview Ave, | MOUNT MARTHA | NSW   | 5085     | 3251             | 1 Fairview Ave,  | MOUNT MARTHA | SA          | 5085           | 2017-02-28 19:23:00 | 25      | 0         | NULL     | NULL              | 4               | 1        | 0           | Unknown   | Unknown      | NULL         | 2017-03-03 14:44:02.143 | amandd01           | 2017-03-03 00:00:00.000 | NULL       | 2018-10-07 00:00:00.000 | 2018-10-07 00:00:00.000 | 1        | 0              | 1        | 0        | NULL              | 2                  | NULL        | 1       |
| 1              | 3000001  | -1           | 1            | NULL  | 1979-02-02 00:00:00 | DARIO     | NULL       | JURJEVIC| Male   | 0262581579 | 0400400856 | 1                         | NA    | 2007-01-05 00:00:00 | 2007-01-05 18:11:00 | ibrahq01 | 1       | Real      | 1      | NULL            | 6        | NULL         | NULL   | NULL  | NULL     | NULL             | NULL              | NULL         | NULL        | NULL            | 2013-12-07 09:48:00 | 109     | 0         | NULL     | NULL              | -1              | 1        | 10          | Inbound Call - New Lead | Inbound Call - New Lead | NULL         | NULL            | NULL       | NULL       | NULL               | NULL                | 2025-04-09 00:00:00.000 | 2025-04-09 00:00:00.000 | 1        | 10              | 0        | 0        | NULL              | 1                  | 109        | 0       |
| 1              | 3000002  | -1           | 1            | NULL  | 2007-01-05 00:00:00 | LARA      | NULL       | JURJEVIC| Female | NULL   | NULL   | 1                         | NA    | 2007-01-05 00:00:00 | 2007-01-05 18:11:00 | ibrahq01 | 1       | Real      | 0      | NULL            | 6        | NULL         | NULL   | NULL  | NULL     | NULL             | NULL              | NULL         | NULL        | NULL            | 2016-06-23 12:08:00 | 109     | 0         | NULL     | NULL              | -1              | 0        | 10          | Inbound Call - New Lead | Inbound Call - New Lead | NULL         | NULL            | NULL       | NULL       | NULL               | NULL                | 2025-04-09 00:00:00.000 | 2025-04-09 00:00:00.000 | 1        | 10              | 0        | 0        | NULL              | 1                  | 109        | 0       |
| 1              | 3000003  | -1           | 1            | NULL  | 2007-01-05 00:00:00 | TIANA-ROSE| NULL       | JURJEVIC| Female | NULL   | NULL   | 1                         | NULL  | 2007-01-05 00:00:00 | 2007-01-05 18:11:00 | ibrahq01 | 1       | Real      | 0      | NULL            | 6        | NULL         | NULL   | NULL  | NULL     | NULL             | NULL              | NULL         | NULL        | NULL            | 2015-04-10 10:11:00 | 109     | 0         | NULL     | NULL              | -1              | 0        | 10          | Inbound Call - New Lead | Inbound Call - New Lead | NULL         | NULL            | NULL       | NULL       | NULL               | NULL                | 2025-04-09 00:00:00.000 | 2025-04-09 00:00:00.000 | 1        | 10              | 0        | 0        | NULL              | 1                  | 109        | 0       |


## 1. Total number of records:

```sql
SELECT COUNT(*) AS TotalRecords FROM [HollardDW].[dbo].[DimClient];
```
TotalRecords
17362666

----------

## 2. List of columns with NULL value counts:

```sql
SELECT 
    COUNT(*) AS TotalRecords,
    SUM(CASE WHEN Email IS NULL THEN 1 ELSE 0 END) AS NullEmails,
    SUM(CASE WHEN PhoneM IS NULL THEN 1 ELSE 0 END) AS NullPhoneM,
    SUM(CASE WHEN DOB IS NULL THEN 1 ELSE 0 END) AS NullDOBs
FROM [HollardDW].[dbo].[DimClient];
```
TotalRecords	NullEmails	NullPhoneM	NullDOBs
17362666	1939172	1679514	3016780

----------

## 3. Number of distinct clients by Email:

```sql
SELECT COUNT(DISTINCT Email) AS DistinctEmails FROM [HollardDW].[dbo].[DimClient];
```
DistinctEmails
6586002

----------

## 5. Distribution of leads vs. non-leads:

```sql
SELECT IsLead, COUNT(*) AS Count
FROM [HollardDW].[dbo].[DimClient]
GROUP BY IsLead;
```
IsLead	Count
NULL	7723
0	775779
1	16582253

----------

## 6. Clients by brand:

```sql
SELECT BrandName, COUNT(*) AS ClientCount
FROM [HollardDW].[dbo].[DimClient]
GROUP BY BrandName
ORDER BY ClientCount DESC;
```
BrandName	ClientCount
Real	4547906
RSPCA	2589715
ASIA	1880727
Woolworths	1745901
Medibank	1674785
Unknown	1318078
Multi	993663
Health	894375
Guardian	448844
Budget	433069
OneChoice	191987
ahm	142594
Aussie	135495
NZ Seniors	111146
Guide Dogs	100486
SPCA	89693
Prime Pet	55248
Kogan	11780
Chubb	261
Guardian Platinum	2

----------

## 7. Clients per partner:

```sql
SELECT PartnerID, COUNT(*) AS ClientCount
FROM [HollardDW].[dbo].[DimClient]
GROUP BY PartnerID
ORDER BY ClientCount DESC;
```
PartnerID	ClientCount
0	14159650
1	2723346
2	269370
3	213389

----------

## 8. How many Medibank members exist:

```sql
SELECT IsMedibankMember, COUNT(*) AS Count
FROM [HollardDW].[dbo].[DimClient]
GROUP BY IsMedibankMember;
```
IsMedibankMember	Count
0	14511164
1	2854591

----------

## 9. Client statuses distribution:

```sql
SELECT ClientStatusID, COUNT(*) AS Count
FROM [HollardDW].[dbo].[DimClient]
GROUP BY ClientStatusID;
```
ClientStatusID	Count
NULL	67656
-1	15165714
1	41560
2	84959
3	3
4	1893816
5	111875
7	172

----------

## 10. Clients created per month (based on CreationDate):

```sql
SELECT FORMAT(CreationDate, 'yyyy') AS Year, COUNT(*) AS ClientCount
FROM [HollardDW].[dbo].[DimClient]
GROUP BY FORMAT(CreationDate, 'yyyy')
ORDER BY Year;
```
Year	ClientCount
2005	1235
2006	1754
2007	20488
2008	192328
2009	812130
2010	1132407
2011	861662
2012	1542710
2013	1525015
2014	1562196
2015	1450232
2016	1418801
2017	1293317
2018	1233871
2019	904935
2020	730577
2021	667890
2022	576236
2023	690207
2024	590800
2025	156964

----------

## 11. Clients with first contact within 7 days of creation:

```sql
SELECT COUNT(*) AS ContactWithin7Days
FROM [HollardDW].[dbo].[DimClient]
WHERE DATEDIFF(DAY, CreationDate, dtmFirstContact) <= 7;
```
ContactWithin7Days
8036075

----------

## 12. Average days between creation and outbound contact:

```sql
SELECT 
  AVG(CAST(DATEDIFF(DAY, CreationDate, dtmOutbound) AS BIGINT)) AS AvgDaysToOutbound
FROM 
  [HollardDW].[dbo].[DimClient]
WHERE 
  dtmOutbound IS NOT NULL
  AND CreationDate IS NOT NULL;
```
AvgDaysToOutbound
233

----------

## 13. Top suburbs by client count:

```sql
SELECT Suburb, COUNT(*) AS Count
FROM [HollardDW].[dbo].[DimClient]
GROUP BY Suburb
ORDER BY Count DESC
OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;
```
Suburb	Count
NULL	5521243
	2230565
MELBOURNE	22517
EPPING	21629
BLACKTOWN	21196
CRAIGIEBURN	20271
RESERVOIR	18807
HOPPERS CROSSING	18734
WERRIBEE	18724
PAKENHAM	18151

----------

## 14. Clients with both phone numbers missing:

```sql
SELECT COUNT(*) AS NoPhoneClients
FROM [HollardDW].[dbo].[DimClient]
WHERE PhoneH IS NULL AND PhoneM IS NULL;
```
NoPhoneClients
68840

----------

## 15. Clients missing both postal and primary addresses:

```sql
SELECT COUNT(*) AS NoAddressClients
FROM [HollardDW].[dbo].[DimClient]
WHERE AddressLine1 IS NULL AND PostalAddressLine1 IS NULL;
```
NoAddressClients
4921985

----------

## 16. Clients with invalid emails (no '@'):

```sql
SELECT COUNT(*) AS InvalidEmails
FROM [HollardDW].[dbo].[DimClient]
WHERE Email IS NOT NULL AND Email NOT LIKE '%@%';
```
InvalidEmails
4927978

----------

## 17. DOB distribution (age buckets):

```sql
SELECT 
    CASE 
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) < 18 THEN 'Under 18'
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) BETWEEN 18 AND 30 THEN '18-30'
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) BETWEEN 31 AND 50 THEN '31-50'
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) > 50 THEN '50+'
        ELSE 'Unknown'
    END AS AgeGroup,
    COUNT(*) AS Count
FROM [HollardDW].[dbo].[DimClient]
GROUP BY 
    CASE 
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) < 18 THEN 'Under 18'
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) BETWEEN 18 AND 30 THEN '18-30'
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) BETWEEN 31 AND 50 THEN '31-50'
        WHEN DATEDIFF(YEAR, DOB, GETDATE()) > 50 THEN '50+'
        ELSE 'Unknown'
    END;
```
AgeGroup	Count
18-30	758564
31-50	5394647
50+	8152597
Under 18	43135
Unknown	3016812

----------