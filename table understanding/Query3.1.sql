--	What is the average number of sales calls required to close a sale?


-- So the logic is simple now, I need to fint the quoteid time and sale time for the client and count the number of calls in that timeframe. It should be the number of calls per application where the sale was successful.
-- I have sale, sale time, clientid, quoteid from fact sales activity and number of calls from ccmscallog. I need to find the quote date. Quote date is also in fact sale activity
-- Problem with above logic - for clientid 6750936, the factsale shows that quotedatetime = 2025-04-28 15:13:00.000 and saledatetime = 2025-04-28 15:27:00.000
 -- While the ccmscalllog shows call from 
--dtmCallStart				dtmCallEnd
--2025-04-28 15:04:45.000	2025-04-28 15:29:02.000
--2025-04-28 15:30:04.000	2025-04-28 15:32:50.000
--2025-04-28 15:30:02.000	2025-04-28 15:31:10.000

--So according to above logic, it is not contained between quotedate and saledate.
--Maybe take ranges ?


-- Not taking this logic since it has proximity and not certainty.

--Instead

--select * from evolve.dbo.tblClientAttemptContactHistory lh
--where dtmClosed is null and dtmLastModified is null
--order by clientid, noofattempts

--select * from HollardDW.dbo.FactCCMSCallLogCTI
--where clientid=27145884
--order by dateid

--select * from evolve.dbo.tblClientAttemptContactHistory lh
--inner join  evolve.dbo.tblWorkItem wi
--on lh.WorkItemID=wi.WorkItemID
--where clientid=27145884
--order by dtminserted

--Took the above both queries and found something that might solve our problem.
--So we wanted that redirects be treated as 1 and no answer as individual
--What I saw is that contact history table has the summary of ccms table

--So for the clientid = 27085245:
--select * from HollardDW.dbo.FactCCMSCallLogCTI
--where clientid=27085245
--order by dateid
--select * from evolve.dbo.tblClientAttemptContactHistory lh
--inner join  evolve.dbo.tblWorkItem wi
--on lh.WorkItemID=wi.WorkItemID
--where clientid=27085245
--order by dtminserted

--the contact history shows 4 records with 8 attempts total.
--The first row can be spot by seeing the dtm inserted and the last one by either dtmclosed or modified
--I checked that both dtmclosed and modified have the same value if not null
--Usually the dtminserted will be minutes after dtmcallend from ccms for first row and dtm closed / modified will be minutes after ccms dtmcallend for last row
--If in between those rows, there has been a redirect then the number of attempts in contact history will be 1
--Else it will be the times it has been contacted.

--For clientid = 27145884, where dtmclosed and modified are null, there is no entry for that in ccms, so we shouldnt take that as well
--select * from HollardDW.dbo.FactCCMSCallLogCTI
--where clientid=27145884
--order by dateid
--select * from evolve.dbo.tblClientAttemptContactHistory lh
--inner join  evolve.dbo.tblWorkItem wi
--on lh.WorkItemID=wi.WorkItemID
--where clientid=27145884
--order by dtminserted

--So ccms and contacthistory are validated

How many rows have less ccms records than contact history

WITH ccms_counts AS (
    SELECT clientid, COUNT(*) AS ccms_count
    FROM HollardDW.dbo.FactCCMSCallLogCTI
    WHERE dateid > '2020-01-01'
    GROUP BY clientid
),
history_counts AS (
    SELECT clientid, SUM(NoofAttempts) AS contact_history_count
    FROM evolve.dbo.tblClientAttemptContactHistory
    WHERE dtminserted > '2020-01-01'
    GROUP BY clientid
)
SELECT h.clientid, cc.ccms_count, h.contact_history_count
FROM history_counts h
LEFT JOIN ccms_counts cc ON h.clientid = cc.clientid
WHERE ISNULL(cc.ccms_count, 0) < h.contact_history_count
  AND cc.ccms_count IS NOT NULL
  AND EXISTS (
      SELECT 1
      FROM HollardDW.dbo.FactSalesActivity fs
      WHERE fs.clientid = h.clientid
        AND fs.sales = 1
  )




select * from HollardDW.dbo.FactCCMSCallLogCTI
where clientid=7060336
order by dateid
select * from evolve.dbo.tblClientAttemptContactHistory lh
inner join  evolve.dbo.tblWorkItem wi
on lh.WorkItemID=wi.WorkItemID
where clientid=7060336
order by dtminserted


-- So the logic will now be that I will see the clientid and quoteid which made a sale and for that client id for the last 30 days from saledatetimeid see the number of attempts in contact history table.
-- So we are assuming that 1 clientid has 1 quoteid in last 30 days or rather 1 sell. Like it can have more quotes but 1 application I meant.


WITH Sales AS (
    SELECT clientid, quoteid, saledatetimeid
    FROM HollardDW.dbo.FactSalesActivity
    WHERE sales = 1
),
ContactHistory AS (
    SELECT 
        clientid,
        NoofAttempts,
        ISNULL(dtmlastmodified, ISNULL(dtmclosed, dtminserted)) AS activity_date
    FROM evolve.dbo.tblClientAttemptContactHistory
)
SELECT 
    s.clientid,
    s.quoteid,
    s.saledatetimeid,
    SUM(ch.NoofAttempts) AS total_calls
FROM Sales s
JOIN ContactHistory ch
    ON s.clientid = ch.clientid
    AND CAST(ch.activity_date AS DATE) BETWEEN DATEADD(DAY, -30, CAST(s.saledatetimeid AS DATE)) AND CAST(s.saledatetimeid AS DATE)
GROUP BY s.clientid, s.quoteid, s.saledatetimeid
ORDER BY total_calls DESC;




WITH Sales AS (
    SELECT clientid, quoteid, saledatetimeid
    FROM HollardDW.dbo.FactSalesActivity
    WHERE sales = 1
),
ContactHistory AS (
    SELECT 
        clientid,
        NoofAttempts,
        ISNULL(dtmlastmodified, ISNULL(dtmclosed, dtminserted)) AS activity_date
    FROM evolve.dbo.tblClientAttemptContactHistory
),
SalesWithAttempts AS (
    SELECT 
        s.clientid,
        s.quoteid,
        s.saledatetimeid,
        SUM(ch.NoofAttempts) AS total_calls
    FROM Sales s
    JOIN ContactHistory ch
        ON s.clientid = ch.clientid
        AND CAST(ch.activity_date AS DATE) BETWEEN DATEADD(DAY, -30, CAST(s.saledatetimeid AS DATE)) AND CAST(s.saledatetimeid AS DATE)
    GROUP BY s.clientid, s.quoteid, s.saledatetimeid
),
Bucketed AS (
    SELECT 
        *,
        CASE 
            WHEN total_calls = 1 THEN '1'
            WHEN total_calls = 2 THEN '2'
            WHEN total_calls = 3 THEN '3'
            WHEN total_calls = 4 THEN '4'
            WHEN total_calls = 5 THEN '5'
            WHEN total_calls = 6 THEN '6'
            WHEN total_calls = 7 THEN '7'
            WHEN total_calls = 8 THEN '8'
            WHEN total_calls = 9 THEN '9'
            WHEN total_calls = 10 THEN '10'
            WHEN total_calls BETWEEN 11 AND 15 THEN '11-15'
            WHEN total_calls BETWEEN 16 AND 20 THEN '16-20'
            WHEN total_calls BETWEEN 21 AND 25 THEN '21-25'
            WHEN total_calls BETWEEN 26 AND 30 THEN '26-30'
            ELSE '31+'
        END AS call_bucket
    FROM SalesWithAttempts
)
SELECT 
    call_bucket,
    COUNT(*) AS num_sales,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS percent_of_sales
FROM Bucketed
GROUP BY call_bucket
ORDER BY 
    CASE 
        WHEN call_bucket = '1' THEN 1
        WHEN call_bucket = '2' THEN 2
        WHEN call_bucket = '3' THEN 3
        WHEN call_bucket = '4' THEN 4
        WHEN call_bucket = '5' THEN 5
        WHEN call_bucket = '6' THEN 6
        WHEN call_bucket = '7' THEN 7
        WHEN call_bucket = '8' THEN 8
        WHEN call_bucket = '9' THEN 9
        WHEN call_bucket = '10' THEN 10
        WHEN call_bucket = '11-15' THEN 11
        WHEN call_bucket = '16-20' THEN 12
        WHEN call_bucket = '21-25' THEN 13
        WHEN call_bucket = '26-30' THEN 14
        ELSE 15
    END;


WITH Sales AS (
    SELECT clientid, quoteid, saledatetimeid, suminsured
    FROM HollardDW.dbo.FactSalesActivity
    WHERE sales = 1
),
ContactHistory AS (
    SELECT 
        clientid,
        NoofAttempts,
        ISNULL(dtmlastmodified, ISNULL(dtmclosed, dtminserted)) AS activity_date
    FROM evolve.dbo.tblClientAttemptContactHistory
),
ContactAttempts AS (
    SELECT 
        s.clientid,
        s.quoteid,
        s.saledatetimeid,
        s.suminsured,
        ch.activity_date,
        ch.NoofAttempts
    FROM Sales s
    JOIN ContactHistory ch
        ON s.clientid = ch.clientid
        AND CAST(ch.activity_date AS DATE) BETWEEN DATEADD(DAY, -30, CAST(s.saledatetimeid AS DATE)) AND CAST(s.saledatetimeid AS DATE)
),
Aggregated AS (
    SELECT 
        clientid,
        quoteid,
        COUNT(*) AS num_contacts_before_sale
    FROM ContactAttempts
    GROUP BY clientid, quoteid
)
SELECT 
    ca.clientid,
    ca.quoteid,
    ca.saledatetimeid,
    ca.activity_date,
    ca.NoofAttempts,
    ca.suminsured,
    ag.num_contacts_before_sale
FROM ContactAttempts ca
JOIN Aggregated ag
    ON ca.clientid = ag.clientid AND ca.quoteid = ag.quoteid
ORDER BY ca.clientid, ca.saledatetimeid, ca.activity_date;


