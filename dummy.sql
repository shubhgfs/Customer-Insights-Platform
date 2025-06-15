SELECT top 100 *
FROM evolvekpi.dbo.tblMaster_CIP
WHERE
    Brand = 'Real'
  AND ProductType = 'Life'



  select * from evolve.dbo.tblproduct where ProductTypeID=1 and BrandID=1 and IsActive=1



select * from [EvolveKPI].[dbo].[tblUnderwritingImpact_CIP]
FROM 
    [HollardDW].[dbo].[FactSalesActivity] fs
LEFT JOIN 
    [HollardDW].[dbo].[FactUWAction] uw
    ON fs.ClientID = uw.ClientID
LEFT JOIN
	[HFSUnderwriting].[dbo].[ProductParentChildMapping] prodpcm
	on fs.productcode = prodpcm.ExternalProductId
LEFT JOIN
	[Evolve].[dbo].[tblProductType] pt
	on fs.ProductTypeID = pt.ProductTypeID


