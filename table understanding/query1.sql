-- How many calls did it take to make a sale for a customer, male and more than 30, between 3rd to 25th November 2024 ?

-- SQL Query to Calculate Calls Before Sale
-- The question asks for how many calls it took to make a sale for male customers over 30 years old between November 3-25, 2024. Let me create a SQL query that connects the call logs to sales data for this specific customer segment.

-- Explanation:
-- First CTE (MaleClientsOver30): Identifies male customers who are over 30 years old as of November 3, 2024.

-- Second CTE (SalesInPeriod): Finds successful sales (Sales > 0) made to these customers between November 3-25, 2024.

-- Third CTE (CallsPerSale): For each sale, counts how many calls were made to that customer in the 90 days before the sale date. This helps focus on calls that were likely related to the sales process.

-- Final query: Calculates the average number of calls required to make a sale, along with minimum and maximum values to show the range. Also provides the total number of qualifying sales for context.

-- This query will provide insights into the typical call effort required to close sales with this customer segment during the specified time period.

WITH MaleClientsOver30 AS (
    -- Identify male customers who are over 30 years old on Nov 3, 2024
    SELECT 
        ClientID
    FROM 
        [HollardDW].[dbo].[DimClient]
    WHERE 
        Gender = 'Male' 
        AND DATEDIFF(YEAR, DOB, '2024-11-03') > 30
),
SalesInPeriod AS (
    -- Find sales made to these customers within the specified date range
    SELECT 
        fs.ClientID,
        fs.QuoteID,
        fs.SaleDateTimeID
    FROM 
        [HollardDW].[dbo].[FactSalesActivity] fs
    INNER JOIN 
        MaleClientsOver30 mc ON fs.ClientID = mc.ClientID
    WHERE 
        (fs.DateID BETWEEN '2024-11-03' AND '2024-11-25'
         OR fs.SaleDateTimeID BETWEEN '2024-11-03 00:00:00' AND '2024-11-25 23:59:59')
        AND fs.Sales > 0  -- Only count successful sales
),
CallsPerSale AS (
    -- Count calls made to each customer before their sale date
    -- Only considering calls within 90 days before the sale
    SELECT 
        s.ClientID,
        s.QuoteID,
        COUNT(c.ID) AS CallCount
    FROM 
        SalesInPeriod s
    LEFT JOIN 
        [HollardDW].[dbo].[FactCCMSCallLogCTI] c ON s.ClientID = c.ClientId
                                                AND c.dtmCallStart < s.SaleDateTimeID
                                                AND c.DateID >= DATEADD(DAY, -90, CAST(s.SaleDateTimeID AS DATE))
    GROUP BY 
        s.ClientID, s.QuoteID
)
-- Calculate average, minimum, and maximum calls required to make a sale
SELECT 
    AVG(CAST(CallCount AS FLOAT)) AS AvgCallsPerSale,
    MIN(CallCount) AS MinCallsPerSale,
    MAX(CallCount) AS MaxCallsPerSale,
    COUNT(*) AS TotalSales
FROM 
    CallsPerSale;

-- Output 
-- AvgCallsPerSale	MinCallsPerSale	MaxCallsPerSale	TotalSales
-- 2.19935170178282	 0	38	2468