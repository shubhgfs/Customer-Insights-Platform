-- Which specific underwriting topics (e.g., pre-existing conditions, family history mentioned in calls) most frequently lead to non-conversion?

--So over here we are trying to find the underwriting topic which has the least sale conversion rate.
--So basically groupby the underwriting condition.
--Least frequent lead to non conversion means the less % of people who called for quotes but did not buy
--So sales = 0 but they do have a quote id
--So for lead conversion data, I can see the fact sales activity table for it
--For knowing the underwriting topic, I can see the factuw tables.
--Lets dive in more to find for that table.

-- The table [HollardDW].[dbo].[FactUWQuestionAnswer] follows the hierarchy QuestionSetInstanceId, sectionid, QuestionId, QuestionSequence where each questionsetinstanceid has sections and each section has questions in sequence to be asked.

--The `FactUWAction` table captures detailed underwriting actions and client responses during the insurance application process. It includes key attributes such as client demographics (e.g., gender, smoking status), product
--information (e.g., `ProductCode`, `BenefitAmount`), and the results of various underwriting questions (`QuestionID`, `AnswerValue`). Additionally, it tracks the status of the underwriting process (`UWStatus`, `ActionType`,
--`DeclineReason`), the reason for any exclusions or declines, and action types taken by the insurer (e.g., `Loading`, `Exclusion`). This table is crucial for understanding underwriting decisions, policy actions, and the overall
--process flow.                    

--The `FactUWProcess` table summarizes the outcomes of the underwriting process at a high level for each insurance application. It captures product and client details (`ProductCode`, `ClientID`, `UWProductType`), the outcome of the
--process (`UWOutcome`), and whether the sale was completed by the system or the underwriter (`SystemSale`, `RUWSale`). It also includes decline and no-sale indicators, the reinsurer involved, and the origin of the record
--(`CreatedBy`, `InsertedDate`). This table is key for tracking overall underwriting performance, clean skin approvals, and process completions over time.

--The `FactUWOutcome` table captures the final underwriting decisions at the benefit level for each application (`QuestionSetInstanceID`). It records whether the process was straight-through (`IsSTP`), the action taken (`ActionType`),
--and a descriptive reason (`ActionTypeText`) such as medical conditions leading to a decline. Each row links to a specific product and benefit combination, with metadata including gender, smoker status, and timestamps
--(`DateTimeAddedID`). This table is essential for identifying decline patterns and understanding underwriting outcomes across products.

--The `FactUWQuestionAnswer` table logs detailed responses to underwriting questions for each client (`ClientID`) and application (`QuestionSetInstanceId`). It includes the section and question identifiers, types (e.g., Radio,
--TextBox), and the answers provided (e.g., "No", "6"). The table also indicates whether the process was straight-through (`IsSTP`), and whether the answer is the most current (`IsCurrent`). This data is critical for assessing risk
--and decision-making during the underwriting process.

--The `FactUnderwriting` table captures weekly aggregated data related to insurance underwriting activities. It includes information about the product (`ProductCode`, `ProductSetID`), brand, sales channel, membership status
--(`IsMedibankMember`), and the operational unit handling the application (e.g., Call Centre). Key metrics such as the number of quotes and actions taken (e.g., "Accepted", "Accepted - Exclusions") are tracked over time using
--`WeekStarting`, `WeekEnding`, and financial year boundaries. This table supports performance monitoring and trend analysis across different channels and time periods.

--The `FactUnderwritingActivity` table logs detailed, individual-level underwriting interactions. Each record captures client-specific actions such as `Action_Taken` (e.g., "Accepted") along with metadata like `UserID`, `ProductCode`,
--`Operational_Unit`, and source-related fields such as `SourceID` and `CampaignBatchID`. It also includes sales channel data (`ChannelID`, `ChannelID_PartnerReporting`) and whether the client is a Medibank member. This granular data
--supports micro-level analysis of underwriting workflows and campaign performance across different user activities.


--So to group by underwriting topics, I can group by section or sectionid.
--Question - What is questionsetinstanceID and why does same clientid have multiple of it ? 
--Seeing for QuestionSetInstanceId=129 and clientid=3410515, I can confirm that as soon as something is not met in uw, it is declined at that question itself.
--That causes the uw status in [HollardDW].[dbo].[FactUWAction] to be declined for that section telling us that it failed at that underwriting topic.
--The QuestionSetInstanceStatus in [FactUWAction] should be complete because the other ones show loading and UW - Complete - Client undecided and uw status as approved. Should confirm why so with Devashish. --> This means that the uw approved the application but the customer is deciding their call and can answer before the quote expiration date.

--Always focus on the latest application for the same clientid or application because the system can be buggy like the clientid=3410515. The last application for that month only.


--So now I need to search for 0 sales but quotes in fs, joint those client ids to uwaction where questionset is complete and uwstatus is decline and then groupby the sections to find the lowest conversion rates.

--select dateid, quoteid, fs.productcode, fs.clientid, fs.brandid, questionsetid, sectionid, section, Question, MainLeadUpQuestionID, MainLeadUpQuestion, AnswerValue
--from [HollardDW].[dbo].[FactSalesActivity] fs
--left join [HollardDW].[dbo].[FactUWAction] uwa
--on fs.clientid=uwa.ClientID
--where fs.sales=0
--and fs.quotes>0
--and uwstatus='Decline'
--and QuestionSetInstanceStatus = 'Complete'

SELECT 
    uwa.SectionID,
    uwa.Section,
	uwa.Question,
    COUNT(DISTINCT fs.ClientID) AS DeclinedClients_NoSales,
    COUNT(DISTINCT fs.QuoteID) AS AffectedQuotes
FROM 
    [HollardDW].[dbo].[FactSalesActivity] fs
LEFT JOIN 
    [HollardDW].[dbo].[FactUWAction] uwa
    ON fs.ClientID = uwa.ClientID
WHERE 
    fs.Sales = 0
    AND fs.Quotes > 0
    AND uwa.UWAppStatus = 'Declined'
    AND uwa.QuestionSetInstanceStatus = 'Complete'
GROUP BY 
    uwa.SectionID, uwa.Section, uwa.Question
ORDER BY 
    DeclinedClients_NoSales DESC;


select * from [HollardDW].[dbo].[FactUWAction]
where clientid=3410515

--Randomly pick up 10 questions and get the frequency of their answers.
--The analysis is seeing that is the decline due to only 1 question or combination of multiple questions.




-- Question 1 - BMI
select AnswerValue, DeclineReason from [HollardDW].[dbo].[FactUWAction] where Question = 'BMI' order by AnswerValue
--0.3-98.75 range of values


select * from   [HollardDW].[dbo].[FactUWAction] uwa  where uwa.UWStatus = 'Decline'
    AND uwa.QuestionSetInstanceStatus = 'Complete' order by clientid


-- Question 2 - Is your condition a form of schizophrenia, bipolar or psychotic disorder?
select clientid, AnswerValue, DeclineReason from [HollardDW].[dbo].[FactUWAction] uwa where Question = 'Is your condition a form of schizophrenia, bipolar or psychotic disorder?'
and uwa.UWStatus = 'Decline'
    AND uwa.QuestionSetInstanceStatus = 'Complete' order by AnswerValue
--0.3-98.75 range of values

select distinct actionvalue, DeclineID, DeclineReason from [HollardDW].[dbo].[FactUWAction] uwa  where actionvalue='865'
and uwa.UWAppStatus = 'Declined'
    AND uwa.QuestionSetInstanceStatus = 'Complete'
	order by questionsetinstanceid, QuestionSectionSequence 

SELECT 
    *
FROM 
    [HollardDW].[dbo].[FactUWAction] uwa
WHERE 
    uwa.UWAppStatus = 'Declined'
    AND uwa.QuestionSetInstanceStatus = 'Complete'
ORDER BY 
    uwa.ClientID,
	StartDateTimeID,
    ActionValue;

select * from [HollardDW].[dbo].[FactUWAction] uwa where clientid= 5419056  -- 3003827


-- Final one
SELECT 
    uwa.Section,
    uwa.Question,
    uwa.declinereason,
    COUNT(DISTINCT fs.ClientID) AS DeclinedClients_NoSales,
    COUNT(DISTINCT fs.QuoteID) AS AffectedQuotes
FROM 
    [HollardDW].[dbo].[FactSalesActivity] fs
LEFT JOIN 
    [HollardDW].[dbo].[FactUWAction] uwa
    ON fs.ClientID = uwa.ClientID
LEFT JOIN
	[HFSUnderwriting].[dbo].[ProductParentChildMapping] prodpcm
	on fs.productcode = prodpcm.ExternalProductId
WHERE 
    fs.Sales = 0
    AND fs.Quotes > 0
    AND uwa.UWAppStatus = 'Declined'
    AND uwa.QuestionSetInstanceStatus = 'Complete'
	AND IsDecline=1
	AND iscurrent=1
	AND prodpcm.ExternalProductId is null
GROUP BY 
    uwa.Section, uwa.Question, uwa.DeclineReason
ORDER BY 
    DeclinedClients_NoSales DESC;

select * from hfsunderwriting.dbo.product --description id
SELECT *
  FROM [HFSUnderwriting].[dbo].[ProductParentChildMapping]
  where id<>1
  --childproductid

-- groupby brand and product. adjust for pivot and non pivot products. We want to see that if a questionset instance has more than 1 decline.


-- SELECT 
--     uwa.QuestionSetInstanceID,
--     uwa.DeclineID,
-- 	uwa.DeclineReason
-- FROM 
--     [HollardDW].[dbo].[FactUWAction] uwa
-- WHERE 
--     uwa.ClientID IN (
--         SELECT 
--             ClientID
--         FROM 
--             [HollardDW].[dbo].[FactUWAction]
--         GROUP BY 
--             ClientID
--         HAVING 
--             COUNT(DISTINCT DeclineID) > 1
--     )
-- 	and clientid<>3000000
-- ORDER BY 
--     uwa.QuestionSetInstanceID, 
--     uwa.DeclineID;







-- select questionsetinstanceid, * from [HollardDW].[dbo].[FactUWAction] 

-- -- so 1 questionsetinstanceid can have more than 1 decline reasons.
-- where UWProductID=3
-- and declineid is not null
-- order by 1


-- select * from hfsunderwriting.dbo.product


-- SELECT 
--    fs.DateID,
--    fs.QuoteID,
--    fs.ClientID,
--    fs.Sales,
--    fs.SumInsured,
--    fs.Quotes,
--    fs.ARRA,
--    uw.Brand,
--    uw.Gender,
--    uw.IsSmoker,
--    uw.Section,
--    uw.Question,
--    uw.AnswerValue,
--    uw.Occupation,
--    uw.Age,
--    uw.DeclineReason,
--    uw.UWAppStatus,
--    uw.QuestionSetInstanceStatus,
--    uw.IsDecline,
--    uw.IsCurrent,
--    pt.ProductType
-- FROM 
--     [HollardDW].[dbo].[FactSalesActivity] fs
-- LEFT JOIN 
--     [HollardDW].[dbo].[FactUWAction] uwa
--     ON fs.ClientID = uwa.ClientID
-- LEFT JOIN
-- 	[HFSUnderwriting].[dbo].[ProductParentChildMapping] prodpcm
-- 	on fs.productcode = prodpcm.ExternalProductId
-- LEFT JOIN
-- 	[Evolve].[dbo].[tblProductType] pt
-- 	on fs.ProductTypeID = pt.ProductTypeID
-- WHERE 
--     fs.Sales = 0
--     AND fs.Quotes > 0
--     AND uwa.UWAppStatus = 'Declined'
--     AND uwa.QuestionSetInstanceStatus = 'Complete'
-- 	AND IsDecline=1
-- 	AND iscurrent=1
-- 	AND prodpcm.ExternalProductId is null




-- -- BASE DATA QUERY 

DROP TABLE IF EXISTS [EvolveKPI].[dbo].[tblUnderwritingImpact_CIP]
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
INTO [EvolveKPI].[dbo].[tblUnderwritingImpact_CIP]
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

