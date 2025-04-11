# [HollardDW].[dbo].[FactCCMSCallLogCTI]

```sql
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [SourceSystemID]
      ,[ID]
      ,[CallId]
      ,[DateID]
      ,[TelsetLoginID]
      ,[UserId]
      ,[CallHour]
      ,[dtmInserted]
      ,[CallType]
      ,[InboundSource]
      ,[NumberCallTerminated]
      ,[OutboundDialled]
      ,[EvolveAction]
      ,[ClientId]
      ,[dtmCallStart]
      ,[dtmCallEnd]
      ,[CallDuration]
      ,[Extension]
      ,[Line]
      ,[UpdatedFromBlueDB]
      ,[SourceID]
      ,[BrandID]
      ,[CallOutcome]
      ,[GSNConnID]
      ,[RingTime]
      ,[CampaignBatchID]
      ,[PartnerID]
      ,[ProductSetID]
      ,[DispositionId]
      ,[Disposition]
      ,[ClientLeadID]
      ,[SystemID]
      ,[IsCLI]
      ,[DWdtmInserted]
      ,[DWdtmUpdated]
      ,[DWStatusID]
  FROM [HollardDW].[dbo].[FactCCMSCallLogCTI]
```

## Sample Data

| `SourceSystemID` | `ID` | `CallId` | `DateID` | `TelsetLoginID` | `UserId` | `CallHour` | `dtmInserted` | `CallType` | `InboundSource` | `NumberCallTerminated` | `OutboundDialled` | `EvolveAction` | `ClientId` | `dtmCallStart` | `dtmCallEnd` | `CallDuration` | `Extension` | `Line` | `UpdatedFromBlueDB` | `SourceID` | `BrandID` | `CallOutcome` | `GSNConnID` | `RingTime` | `CampaignBatchID` | `PartnerID` | `ProductSetID` | `DispositionId` | `Disposition` | `ClientLeadID` | `SystemID` | `IsCLI` | `DWdtmInserted` | `DWdtmUpdated` | `DWStatusID` |
|------------------|------|----------|----------|-----------------|-----------|------------|---------------|------------|-----------------|------------------------|-------------------|---------------|------------|----------------|--------------|----------------|-------------|-------|---------------------|------------|-----------|---------------|-------------|------------|-------------------|-------------|----------------|----------------|--------------|----------------|------------|---------|-----------------|----------------|--------------|
| 1 | 1 | 12216 | 2010-11-03 | 5457 | AshleO01 | 17 | 2010-11-03 17:37:13.193 | Outbound |  | 0398791381 | 0398791381 | NULL | NULL | 2010-11-03 17:37:12.523 | 2010-11-03 17:46:05.983 | 533 | 1086 | Line 108.0.2.9/1086 | NULL | -1 | -1 | NULL | NULL | NULL | -1 | 0 | -1 | NULL | NULL | NULL | 1 | 0 | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1 |
| 1 | 2 | 15958 | 2010-11-03 | 5042 | TraceB01 | 17 | 2010-11-03 17:37:19.070 | Outbound |  | 0740943143 | 0740943143 | NULL | NULL | 2010-11-03 17:37:18.397 | 2010-11-03 17:37:25.023 | 7 | 1006 | Line 96.0.1.5/1006 | NULL | -1 | -1 | NULL | NULL | NULL | -1 | 0 | -1 | NULL | NULL | NULL | 1 | 0 | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1 |
| 1 | 3 | 15761 | 2010-11-03 | 5360 | KandyL01 | 17 | 2010-11-03 17:37:20.333 | Inbound | 150 | 2000 |  | NULL | NULL | 2010-11-03 17:37:19.680 | 2010-11-03 17:37:24.193 | 5 | 221039 | Line 96.0.2.6/221039 | NULL | -1 | -1 | NULL | NULL | NULL | -1 | 0 | -1 | NULL | NULL | NULL | 1 | 0 | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1 |
| 1 | 4 | 11534 | 2010-11-03 | 5475 | daniev01 | 17 | 2010-11-03 17:37:27.770 | Outbound |  | 0244235188 | 0244235188 | NULL | NULL | 2010-11-03 17:37:27.100 | 2010-11-03 17:37:33.930 | 6 | 1082 | Line 108.0.1.0/1082 | NULL | -1 | -1 | NULL | NULL | NULL | -1 | 0 | -1 | NULL | NULL | NULL | 1 | 0 | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1 |
| 1 | 5 | 14267 | 2010-11-03 | 5610 | PrincM01 | 17 | 2010-11-03 17:37:28.210 | Outbound |  | 0268422047 | 0268422047 | NULL | NULL | 2010-11-03 17:37:27.537 | 2010-11-03 17:41:44.410 | 257 | 1160 | Line 96.1.0.22/1160 | NULL | -1 | -1 | NULL | NULL | NULL | -1 | 0 | -1 | NULL | NULL | NULL | 1 | 0 | 2025-04-06 00:00:00.000 | 2025-04-06 00:00:00.000 | 1 |


### 📊 **1. Total Record Count**
```sql
SELECT  COUNT(*) AS TotalRecords FROM [HollardDW].[dbo].[FactCCMSCallLogCTI];
```
TotalRecords = 104318910

----------

### 📅 **2. Min & Max Dates for Date/Time Columns**
```sql
SELECT  MIN(DateID) AS Min_DateID, MAX(DateID) AS Max_DateID, MIN(dtmInserted) AS Min_dtmInserted, MAX(dtmInserted) AS Max_dtmInserted, MIN(DWdtmInserted) AS Min_DWdtmInserted, MAX(DWdtmInserted) AS Max_DWdtmInserted FROM [HollardDW].[dbo].[FactCCMSCallLogCTI];
```
Min_DateID	Max_DateID	Min_dtmInserted	Max_dtmInserted	Min_DWdtmInserted	Max_DWdtmInserted
2010-11-03	2025-04-08	2010-11-03 17:37:13.193	2025-04-08 20:00:48.583	2018-10-07 00:00:00.000	2025-04-09 00:00:00.000

----------

### 🧍‍♂️ **3. Distinct Users (Telset Login)**
```sql
SELECT  COUNT(DISTINCT TelsetLoginID) AS Distinct_TelsetLoginID FROM [HollardDW].[dbo].[FactCCMSCallLogCTI];
```
Distinct_TelsetLoginID
1788

----------

### 📞 **4. Calls by Type Distribution**
```sql
SELECT CallType, COUNT(*) AS CallCount FROM [HollardDW].[dbo].[FactCCMSCallLogCTI] GROUP  BY CallType ORDER  BY CallCount DESC;
```
CallType	CallCount
Outbound	91941961
Inbound	8616369
Consult	2420036
Internal	1338512
	2026
Transfer	6

----------

### ⌛ **5. Call Duration Stats**
```sql
SELECT  MIN(CallDuration) AS MinDuration, MAX(CallDuration) AS MaxDuration, AVG(CallDuration *  1.0) AS AvgDuration FROM [HollardDW].[dbo].[FactCCMSCallLogCTI];
```
MinDuration	MaxDuration	AvgDuration
-32498	38024	86.414180

----------

### 🧮 **6. Count of Nulls per Column (Dynamic ```sql recommended for full check)**
Example for a few key columns:
```sql
SELECT  SUM(CASE  WHEN CallOutcome IS  NULL  THEN  1  ELSE  0  END) AS Null_CallOutcome, SUM(CASE  WHEN CallDuration IS  NULL  THEN  1  ELSE  0  END) AS Null_CallDuration FROM [HollardDW].[dbo].[FactCCMSCallLogCTI];
```
Null_CallOutcome	Null_CallDuration
16144045	49800

----------

### 📌 **7. Top 10 Frequent Dispositions**
```sql
SELECT TOP 10 Disposition, COUNT(*) AS Frequency FROM [HollardDW].[dbo].[FactCCMSCallLogCTI] GROUP  BY Disposition ORDER  BY Frequency DESC; 
```
Disposition	Frequency
NULL	103242896
Successful Contact	595973
Answering Machine	318298
Do not Contact	78641
Not Right Party Contact	78475
Warm Transfer	4627

----------

### 📆 **8. Record Count by DateID - Year (for time-series analysis)**
```sql
SELECT 
    YEAR(DateID) AS Year,
    COUNT(*) AS RecordsPerYear
FROM [HollardDW].[dbo].[FactCCMSCallLogCTI]
GROUP BY YEAR(DateID)
ORDER BY Year;
```
Year	RecordsPerYear
2010	511275
2011	3284089
2012	4849471
2013	6009829
2014	7493112
2015	7622504
2016	7912971
2017	10079339
2018	12206854
2019	10363850
2020	7883091
2021	6081482
2022	5698776
2023	6156517
2024	6348430
2025	1817320

----------

### 📡 **9. Source Systems Count**
```sql
SELECT SourceSystemID, COUNT(*) AS CountPerSource FROM [HollardDW].[dbo].[FactCCMSCallLogCTI] GROUP  BY SourceSystemID ORDER  BY CountPerSource DESC;
```
SourceSystemID	CountPerSource
1	93188506
2	11130404

----------

### 🧾 **10. Unique Count of Call IDs**
```sql
SELECT  COUNT(DISTINCT CallId) AS Distinct_CallIds FROM [HollardDW].[dbo].[FactCCMSCallLogCTI];
```
Distinct_CallIds
20027

----------

### 📊 **11. Frequency of Each Brand**
```sql
SELECT BrandID, COUNT(*) AS CountPerBrand FROM [HollardDW].[dbo].[FactCCMSCallLogCTI] GROUP  BY BrandID ORDER  BY CountPerBrand DESC;
```
BrandID	CountPerBrand
1	31043788
9	15231688
3	12353190
2	11676542
-1	10616453
11	8052086
0	5394605
17	2108729
7	1830753
16	1176571
1001	1101922
5	1067850
15	686983
13	655824
18	452189
4	445617
10	268072
14	141768
12	14279
6	1

----------

### 🧑‍🤝‍🧑 **12. Number of Distinct ClientLeads**
```sql
SELECT  COUNT(DISTINCT ClientLeadID) AS Distinct_ClientLeadIDs FROM [HollardDW].[dbo].[FactCCMSCallLogCTI];
```
Distinct_ClientLeadIDs
614451

----------

### 🧯 **13. Most Common Call Outcomes**
```sql
SELECT TOP 10 CallOutcome, COUNT(*) AS Frequency FROM [HollardDW].[dbo].[FactCCMSCallLogCTI] GROUP  BY CallOutcome ORDER  BY Frequency DESC;
```
CallOutcome	Frequency
SuccessfulContact	22680234
VoiceMail	22584983
NoAnwser	21110888
NULL	16144045
InboundCall	8303138
DestinationBusy	4621630
CancelledByUser	4084329
WrongNumber	3896548
UnsuccessfulCallback	554449
InboundCallRejected	209361

----------


## Table Description

The `[HollardDW].[dbo].[FactCCMSCallLogCTI]` table stores call center interactions, capturing both inbound and outbound calls with detailed information about timing, duration, agents, outcomes, and related business entities.

## Data Overview

### 📊 Total Record Count
- 104,318,910 records

### 📅 Date Range
- Earliest: 2010-11-03
- Latest: 2025-04-08

### 📞 Call Types Distribution
| Call Type | Count | Percentage |
|-----------|--------|------------|
| Outbound | 91,941,961 | 88.1% |
| Inbound | 8,616,369 | 8.3% |
| Consult | 2,420,036 | 2.3% |
| Internal | 1,338,512 | 1.3% |
| (NULL) | 2,026 | <0.1% |
| Transfer | 6 | <0.1% |

### 🧑‍💼 User Stats
- 1,788 distinct teleset logins

### ⏱️ Call Duration
- Minimum: -32,498 seconds (likely data error)
- Maximum: 38,024 seconds
- Average: 86.41 seconds

### 📱 Top Call Outcomes
| Outcome | Count | Percentage |
|---------|-------|------------|
| SuccessfulContact | 22,680,234 | 21.7% |
| VoiceMail | 22,584,983 | 21.6% |
| NoAnwser | 21,110,888 | 20.2% |
| NULL | 16,144,045 | 15.5% |
| InboundCall | 8,303,138 | 8.0% |

### 🏢 Top Brands
| Brand ID | Call Count |
|----------|------------|
| 1 | 31,043,788 |
| 9 | 15,231,688 |
| 3 | 12,353,190 |
| 2 | 11,676,542 |

## Column Descriptions


| Column Name           | Description |
|-----------------------|-------------|
| **SourceSystemID**    | Identifier for the source system where the call data originated. Two distinct source systems, with ID 1 being predominant (93,188,506 records). |
| **ID**                | Unique identifier/primary key for each call record within this fact table. |
| **CallId**            | Identifier for the call within the telephony system. 20,027 distinct call IDs. |
| **DateID**            | Date when the call occurred (2010-11-03 to 2025-04-08). |
| **TelsetLoginID**     | Numerical identifier for the teleset device used by the operator. 1,788 distinct teleset logins. |
| **UserId**            | Username of the agent/employee who handled the call (e.g., AshleO01, TraceB01). |
| **CallHour**          | Hour of the day (0–23) when the call occurred. Used for analyzing call volumes. |
| **dtmInserted**       | Timestamp when the call record was inserted into the database. |
| **CallType**          | Call direction classification: Outbound (87.6%), Inbound (8.3%), Consult (2.3%), Internal (1.3%), Transfer (<0.01%), and some NULLs. |
| **InboundSource**     | Source identifier for inbound calls, indicating line or campaign. |
| **NumberCallTerminated** | Phone number where the call was terminated. For inbound, it's the internal number. |
| **OutboundDialled**   | Phone number dialed for outbound calls. Empty for inbound calls. |
| **EvolveAction**      | Action taken within the Evolve system (CRM or policy system). Mostly NULL. |
| **ClientId**          | Identifier linking the call to a specific client. |
| **dtmCallStart**      | Timestamp when the call started. |
| **dtmCallEnd**        | Timestamp when the call ended. |
| **CallDuration**      | Duration in seconds. Average: 86.4 seconds. Some negative values (likely system errors). |
| **Extension**         | Internal phone extension of the agent. |
| **Line**              | Phone line used for the call (often shows IP + extension). |
| **UpdatedFromBlueDB** | Flag for updates from BlueDB system. |
| **SourceID**          | Possibly related to marketing campaigns or call sources. Mostly -1. |
| **BrandID**           | Identifier for the insurance brand. Brand 1 has highest volume (31,043,788 calls). |
| **CallOutcome**       | Result of the call: SuccessfulContact (21.7%), VoiceMail (21.6%), NoAnswer (20.2%), InboundCall (8%), 15.5% NULL. |
| **GSNConnID**         | Global Session Network Connection ID. Likely unique in telephony system. |
| **RingTime**          | Duration (in seconds) the phone rang before being answered. |
| **CampaignBatchID**   | Identifier for the marketing campaign batch. |
| **PartnerID**         | Identifier for partner organization (if applicable). |
| **ProductSetID**      | Identifier for the insurance product set discussed. |
| **DispositionId**     | Numeric identifier for call outcome/disposition. |
| **Disposition**       | Textual call outcome. Mostly NULL (98.9%), then "Successful Contact" (0.6%), "Answering Machine" (0.3%). |
| **ClientLeadID**      | Identifier linking the call to a specific sales lead. 614,451 distinct leads. |
| **SystemID**          | Identifier for the system that handled the call. |
| **IsCLI**             | Caller Line Identification available: 0 = No, 1 = Yes. |
| **DWdtmInserted**     | Timestamp when the record was inserted into the data warehouse. |
| **DWdtmUpdated**      | Timestamp when the record was last updated in the warehouse. |
| **DWStatusID**        | Status identifier for the record in the data warehouse. |
