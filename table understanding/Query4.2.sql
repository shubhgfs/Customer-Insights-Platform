-- Compare the average finalized SI per agent.?

WITH ActiveSalesAgents AS (
    SELECT 
        dud.UserID
    FROM 
        [HollardDW].[dbo].[DimUserDay] dud
    WHERE 
        dud.DateID = CAST(GETDATE() AS DATE)
        AND dud.BusinessFunction = 'Sales'
        AND dud.IsActive = 1
),
ExcludedProducts AS (
    SELECT DISTINCT 
        ProductCode
    FROM 
        HollardDW.pbi.tblUWKPIReportDailyPivotProduct
)
SELECT 
    fs.UserID,
    COUNT_BIG(*) AS TotalQuotes,  -- Total quotes per agent
    SUM(fs.SumInsured) AS TotalSumInsured,  -- Total Sum Insured
    CAST(
        SUM(fs.SumInsured) * 1.0 / NULLIF(COUNT_BIG(*), 0)
        AS DECIMAL(18,2)
    ) AS AverageSumInsured  -- Average Sum Insured per quote
FROM 
    [HollardDW].[dbo].[FactSalesActivity] fs
INNER JOIN ActiveSalesAgents asa
    ON fs.UserID = asa.UserID
LEFT JOIN ExcludedProducts ep
    ON fs.ProductCode = ep.ProductCode
WHERE 
    fs.Quotes > 0
    AND ep.ProductCode IS NULL
    AND fs.SumInsured IS NOT NULL  -- Only consider quotes with a Sum Insured value
GROUP BY 
    fs.UserID
ORDER BY 
    AverageSumInsured DESC;  -- Highest average SI at the top
