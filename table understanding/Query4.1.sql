-- Which sales agents have the highest conversion rates?

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
    COUNT_BIG(*) AS TotalQuotes,  -- Use COUNT_BIG for better performance on large tables
    SUM(CASE WHEN fs.Sales = 1 THEN 1 ELSE 0 END) AS TotalSales,
    CAST(
        SUM(CASE WHEN fs.Sales = 1 THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT_BIG(*), 0)
        AS DECIMAL(10,4)
    ) AS SalesConversionRate
FROM 
    [HollardDW].[dbo].[FactSalesActivity] fs
INNER JOIN ActiveSalesAgents asa
    ON fs.UserID = asa.UserID
LEFT JOIN ExcludedProducts ep
    ON fs.ProductCode = ep.ProductCode
WHERE 
    fs.Quotes > 0
    AND ep.ProductCode IS NULL  -- Exclude matching products
GROUP BY 
    fs.UserID
ORDER BY 
    SalesConversionRate DESC;
