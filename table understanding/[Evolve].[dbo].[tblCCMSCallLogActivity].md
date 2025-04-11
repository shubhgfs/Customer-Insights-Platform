# [Evolve].[dbo].[tblCCMSCallLogActivity]

````sql
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [CCMSCallLogActivityID]
  ,[CCMSCallLogID]
  ,[CCMSCallLogActivityTypeId]
  ,[Value]
  ,[CreatedDate]
  ,[CreatedBy]
  FROM [Evolve].[dbo].[tblCCMSCallLogActivity]
````

## Sample Data

`CCMSCallLogActivityID` | `CCMSCallLogID` | `CCMSCallLogActivityTypeId` | `Value` | `CreatedDate` | `CreatedBy`
--- | --- | --- | --- | --- | ---
1 | 76081431 | 1 | 13029200 | 2021-04-15 21:55:25.640 | HFS\EvolveAppProd.svc
2 | 76081434 | 1 | 13029216 | 2021-04-15 22:08:38.073 | HFS\EvolveAppProd.svc
3 | 76081434 | 3 | 13029217 | 2021-04-15 22:10:22.457 | HFS\EvolveAppProd.svc
4 | 76023641 | 5 | 3533889 | 2021-04-16 05:44:08.100 | HFS\EvolveAppProd.svc


Total Records = 1632842
max_date = Yesterday
min_date = 2021-04-15 21:55:25.640
Distinct `CCMSCallLogID` = 987729
Distinct `Value` = 1303661


## Column Description

Based on the table structure from [Evolve].[dbo].[tblCCMSCallLogActivity], I can provide the following descriptions for each column:

`CCMSCallLogActivityID`: Primary key/unique identifier for each call log activity record. This is an auto-incrementing integer that uniquely identifies each entry in the table.

`CCMSCallLogID`: Foreign key that links to the main call log record. This suggests each call can have multiple activities associated with it, creating a one-to-many relationship between calls and activities.

`CCMSCallLogActivityTypeId`: An identifier representing the type of activity that occurred during the call. The values (1, 3, 5 from the sample data) likely correspond to specific activity types (such as call initiation, transfer, notes added, etc.).

`Value`: A reference identifier that appears to link to another entity or record in the system. Based on the count (Distinct Value = 1303661), these likely reference specific customer records, case numbers, or other entities that were involved in the call activity.

`CreatedDate`: Timestamp indicating when the call activity record was created. The data spans from April 15, 2021, to April 8, 2025, with the most recent entry being very current.

`CreatedBy`: The user or system account that created the record. In the sample data, all entries were created by the service account "HFS\EvolveAppProd.svc", suggesting these records are system-generated rather than manually entered.

The table appears to be a detailed activity log for customer service calls at Greenstone Financials Insurance Company, tracking each action or event that occurs during customer interactions through their CCMS (Customer Contact Management System). With over 1.6 million records and nearly 1 million distinct call logs, this represents a comprehensive call activity history for the company.