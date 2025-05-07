--	How does smoker status impact the likelihood of a sale completion and the average finalized SI?

WITH ExcludedProducts AS (
    SELECT DISTINCT 
        ProductCode
    FROM 
        HollardDW.pbi.tblUWKPIReportDailyPivotProduct
),
SalesData AS (
    SELECT 
        fs.ClientID,
        fs.UserID,
        fs.Sales,
        fs.SumInsured
    FROM 
        [HollardDW].[dbo].[FactSalesActivity] fs
    LEFT JOIN ExcludedProducts ep
        ON fs.ProductCode = ep.ProductCode
    WHERE 
        fs.Quotes > 0
        AND ep.ProductCode IS NULL
        AND fs.SumInsured IS NOT NULL
),
SmokerStatus AS (
    SELECT 
        DISTINCT ClientID, 
        CAST(IsSmoker AS VARCHAR(10)) AS IsSmokerStatus
    FROM 
        [HollardDW].[dbo].[FactUWAction]
    WHERE 
        ClientID IS NOT NULL
)
SELECT 
    COALESCE(ss.IsSmokerStatus, 'Unknown') AS SmokerStatus,
    COUNT_BIG(sd.ClientID) AS TotalQuotes,
    SUM(CASE WHEN sd.Sales = 1 THEN 1 ELSE 0 END) AS TotalSales,
    CAST(
        SUM(CASE WHEN sd.Sales = 1 THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT_BIG(sd.ClientID), 0)
        AS DECIMAL(10,4)
    ) AS SalesConversionRate,
    SUM(sd.SumInsured) AS TotalSumInsured,
    CAST(
        SUM(sd.SumInsured) * 1.0 / NULLIF(COUNT_BIG(sd.ClientID), 0)
        AS DECIMAL(18,2)
    ) AS AverageSumInsured
FROM 
    SalesData sd
LEFT JOIN 
    SmokerStatus ss
    ON sd.ClientID = ss.ClientID
GROUP BY 
    ss.IsSmokerStatus
ORDER BY 
    SalesConversionRate DESC;


drop table if exists [EvolveKPI].[dbo].[CIP_Lifestyle_Smoking]
-- Main query: fetch detailed sales activity with client demographic enrichment
SELECT
    fs.DateID,                          -- Date of the sales activity
    fs.ClientID,                        -- Unique identifier for the client
    ua.Gender,                          -- Gender from UW data or fallback later
    ua.Age,                             -- Age from UW data or fallback from DOB
    ua.IsSmokerStatus,                 -- Smoker status ('True', 'False', or 'Unknown')
    ua.Occupation,                      -- Occupation from UW data or fallback from tblOccupation
    ua.OccupationClass,                -- Occupation class (no fallback currently)
    fs.QuoteID,                         -- Unique quote ID
    br.BrandName,                       -- Brand name from Brand table
    pt.ProductType,                     -- Product type from ProductType table
    fs.Quotes,                          -- Number of quotes
    fs.Applications,                    -- Number of applications
    fs.Sales,                           -- Whether the quote converted into a sale (1 = Yes, 0 = No)
    fs.Premium,                         -- Premium amount
    fs.SumInsured,                      -- Finalized sum insured
    fs.ARRA,                            -- Additional Revenue Recognition Amount
    fs.ClientPolicyNumber              -- Client's policy number
INTO [EvolveKPI].[dbo].[CIP_Lifestyle_Smoking]
FROM 
    [HollardDW].[dbo].[FactSalesActivity] fs

-- Join to get Product Type name
LEFT JOIN [Evolve].[dbo].[tblProductType] pt
    ON fs.ProductTypeID = pt.ProductTypeID

-- Join to get Brand name
LEFT JOIN [Evolve].[dbo].[tblBrand] br
    ON fs.BrandID = br.BrandID

-- Join to bring in demographic details (prefer UWAction, fallback handled separately if needed)
LEFT JOIN (
    SELECT 
        DISTINCT 
        f.ClientID,
        -- Use Gender from UW if available
        COALESCE(
				CASE 
					WHEN f.Gender = 'M' THEN 'M'   -- 'M' from FactUWAction
					WHEN f.Gender = 'F' THEN 'F'   -- 'F' from FactUWAction
					WHEN c.Gender = 1 THEN 'M'     -- 1 from tblClient maps to 'M'
					WHEN c.Gender = 2 THEN 'F'     -- 2 from tblClient maps to 'F'
					ELSE NULL
				END,
				'Unknown' -- Default if no gender is found
			) AS Gender,
        -- Use Age from UW if available, otherwise calculate from DOB
        COALESCE(f.Age, DATEDIFF(YEAR, c.DOB, GETDATE())) AS Age,
        -- Use Occupation from UW, fallback from tblOccupation
        COALESCE(f.Occupation, o.OccupationDescription) AS Occupation,
        -- Occupation Class available only from UW
        f.OccupationClass,
        -- Smoker status as string
        CAST(COALESCE(f.IsSmoker, 'Unknown') AS VARCHAR(10)) AS IsSmokerStatus
    FROM 
        [HollardDW].[dbo].[FactUWAction] f
    FULL OUTER JOIN [Evolve].[dbo].[tblClient] c
        ON f.ClientID = c.ClientID
    LEFT JOIN [Evolve].[dbo].[tblOccupation] o
        ON c.OccupationID = o.OccupationID
    WHERE 
        COALESCE(f.ClientID, c.ClientID) IS NOT NULL
) ua
    ON fs.ClientID = ua.ClientID

-- Filter: Only include valid quotes
WHERE 
    fs.Quotes > 0

-- Filter: Exclude product codes listed in KPI exclusion table
    AND fs.ProductCode NOT IN (
        SELECT DISTINCT ProductCode
        FROM HollardDW.pbi.tblUWKPIReportDailyPivotProduct
    )

-- Filter: Ensure finalized Sum Insured exists
    AND fs.SumInsured IS NOT NULL
	AND fs.DateID BETWEEN '2022-01-01' AND '2025-05-01'







