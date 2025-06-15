
DROP TABLE IF EXISTS [EvolveKPI].[dbo].[tblMaster_CIP]
SELECT 
   fs.DateID,
   fs.QuoteID,
   fs.ClientID,
   fs.Sales,
   fs.SumInsured,
   fs.Quotes,
   fs.ARRA,
   uw.Brand,
   pt.ProductType,
   uw.Gender,
   uw.IsSmoker,
   uw.Section,
   uw.Question,
   uw.AnswerValue,
   uw.Occupation,
   uw.Age,
   uw.DeclineReason,
   uw.UWAppStatus,
   uw.QuestionSetInstanceStatus,
   uw.IsDecline,
   uw.IsCurrent
INTO [EvolveKPI].[dbo].[tblMaster_CIP]
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
WHERE 
    prodpcm.ExternalProductId is null
	AND fs.DateID BETWEEN '2022-01-01' AND '2025-05-01'

