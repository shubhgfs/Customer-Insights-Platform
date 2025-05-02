-- What is the average Sum Insured (SI) and sales conversion rate for males vs. females?

--Ok, so average sum insured and sales conversion rates for males vs females.
--So after grouping by males and females, just get the average of sum insured and the sales conversion rates.
--Where do I get the sum insured for individual clients and the sales conversion rates for individual clients.
--The gender is available in dimclient hollard dw
--Which table do I look in for sum insured ?
--FactSalesActivity has ClientID and sum insured column. So I can take those from there.
--Sales Conversion Rate is the % of people converted from lead to sales.
--Hence I can take this also from fact sales activity assuming (crosscheck with Devashish)
--that all the leads are in this table with lead marked as 1 in sales column for sale.

select fs.clientid, sales, suminsured, gender
from [HollardDW].[dbo].[FactSalesActivity] fs
left join [HollardDW].[dbo].[DimClient] cl
on fs.clientid=cl.clientid

-- Ok so after this query I notice something like 
--clientid	sales	suminsured	gender
--10003505	0	0.00	Male
--10003505	1	10000.00	Male

--For the same clientid, there are 2 entries for sale and no sale.
--Should I take both ? Remove the no sale one ?
--Filter out no quote and no applications.

--Lets check the query more in fact sales table

select * from [HollardDW].[dbo].[FactSalesActivity]
where clientid=10003505

--Both the entries has same dateid, quoteid, brand, product. Different rider code.
--The one with sale has less blank columns compared to one with no sale.
--The one with no sale has quoteid but shows 0 quotes and 0 applications.
--So should I consider it ? No I should not

--ProductCode	RiderCode	RiderDescription	IsMandatory
--FEP	DTH	Funeral Insurance	1
--FEP	NOR	No Rider	0
--This is the rider code meaning


--Simply put, a rider provides additional coverage and added protection against risks. Insurance riders are effective add-ons you can choose in addition to your life insurance policy at economical rates. They make your policies robust and broad, covering more than just the cost of your demise.
--google definition of a rider

--I think I should consider both since it is there in this BI table. If it was not to be considered it might not have been added in this BI table.
--I will crosscheck this with Devashish.


SELECT 
    cl.Gender,
    COUNT(*) AS TotalQuotes,
    SUM(CASE WHEN fs.Sales = 1 THEN 1 ELSE 0 END) AS TotalSales,
    AVG(fs.SumInsured) AS Avg_SumInsured,
    CAST(SUM(CASE WHEN fs.Sales = 1 THEN 1.0 ELSE 0 END) / COUNT(*) AS DECIMAL(10,4)) AS SalesConversionRate
FROM [HollardDW].[dbo].[FactSalesActivity] fs
LEFT JOIN [HollardDW].[dbo].[DimClient] cl
    ON fs.ClientID = cl.ClientID
WHERE Quotes > 0
AND Applications > 0
AND ProductTypeID = 1
GROUP BY cl.Gender

--Male has low acceptance rate due to smoking and drinking and hence female conversion rate is expected to be more.
--So products have main product and child product (evolve.dbo.tblproduct), if the customer is declined for main product (primary application) it is pivoted to child product (secondary application). So it might show two rows, 1 with sale and 1 with no sale but in reality we should only take 1 row which says sale leading to overall higher conversion rates.

select * from [HollardDW].[dbo].[FactSalesActivity]Other
 where productcode in ('HIA','HIN')
 and quotes>0 and applications>0
 order by clientid 

select Sales, Quotes, Applications, ProductCode, ClientID, *
from [HollardDW].[dbo].[FactSalesActivity]
where ClientID=7710812
and ProductCode in ('HIA', 'HIN')
and Quotes>0


--Write the earlier query excluding pivot products and write a new query union with earlier one which deals with pivot products considering them as 1 only rather than multiple products.
-- Have no filter for applications because application will only be 1 after which for pivot there will be a quote but no application. Quote 0 application 1 means incomplete underwriting.



SELECT *
  FROM [HFSUnderwriting].[dbo].[ProductParentChildMapping]
  where id<>1


  SELECT dateid, quoteid, productcode, clientid, brandid, sales, quotes, applications, ProductTypeID
FROM [HollardDW].[dbo].[FactSalesActivity]
where suminsured > 0
and quotes > 0
order by Sales






WITH PivotProducts AS (
    SELECT 
        ParentProductId,
        ChildProductId,
        ExternalProductId
    FROM [HFSUnderwriting].[dbo].[ProductParentChildMapping]
    WHERE id <> 1
),
SalesData AS (
    SELECT 
        fs.ClientID,
        fs.ProductCode,
        fs.Sales,
        fs.SumInsured,
        cl.Gender,
        CASE 
            WHEN pp.ParentProductId IS NOT NULL THEN 'Parent'
            WHEN pp.ChildProductId IS NOT NULL THEN 'Child'
            ELSE 'NonPivot'
        END AS ProductType,
        pp.ParentProductId,
        pp.ChildProductId
    FROM [HollardDW].[dbo].[FactSalesActivity] fs
    LEFT JOIN [HollardDW].[dbo].[DimClient] cl
        ON fs.ClientID = cl.ClientID
    LEFT JOIN PivotProducts pp
        ON fs.ProductCode = pp.ExternalProductId
    WHERE fs.Quotes > 0
      AND fs.Applications > 0
      AND fs.ProductTypeID = 1
),
MarkedSales AS (
    SELECT *,
        CASE 
            WHEN ProductType = 'Child' THEN 1
            WHEN ProductType = 'Parent' AND ClientID IN (
                SELECT DISTINCT s.ClientID
                FROM SalesData s
                WHERE s.ProductType = 'Child' AND s.Sales = 1
            ) THEN 0 -- parent ignored if child sale succeeded
            ELSE 1 -- non-pivot or parents with no successful child sale
        END AS IncludeFlag
    FROM SalesData
)

-- Now only consider rows where IncludeFlag = 1
SELECT 
    Gender,
    COUNT(*) AS TotalQuotes,
    SUM(CASE WHEN Sales = 1 THEN 1 ELSE 0 END) AS TotalSales,
    CAST(SUM(CASE WHEN Sales = 1 THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(*),0) AS DECIMAL(10,4)) AS SalesConversionRate,
    AVG(SumInsured) AS Avg_SumInsured
FROM MarkedSales
WHERE IncludeFlag = 1
GROUP BY Gender
ORDER BY Gender;



-- Final one
SELECT 
    cl.Gender,
    COUNT(*) AS TotalQuotes,  -- Total number of quotes for each gender
    SUM(CASE WHEN fs.Sales = 1 THEN 1 ELSE 0 END) AS TotalSales,  -- Total number of sales
    AVG(fs.SumInsured) AS Avg_SumInsured,  -- Average sum insured per quote
    CAST(
        SUM(CASE WHEN fs.Sales = 1 THEN 1.0 ELSE 0 END) / COUNT(*) 
        AS DECIMAL(10,4)
    ) AS SalesConversionRate  -- Sales / Quotes as a decimal
FROM 
    [HollardDW].[dbo].[FactSalesActivity] fs
LEFT JOIN 
    [HollardDW].[dbo].[DimClient] cl
    ON fs.ClientID = cl.ClientID
LEFT JOIN 
    [HFSUnderwriting].[dbo].[ProductParentChildMapping] prodpcm
    ON fs.ProductCode = prodpcm.ExternalProductId
WHERE 
    fs.Quotes > 0  -- Consider only rows where at least one quote was made
    AND prodpcm.ExternalProductId IS NULL  -- Filter out matched products from mapping table
GROUP BY 
    cl.Gender;  -- Aggregate metrics by gender






