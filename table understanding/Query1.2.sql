-- Show me the distribution of SI requested vs. SI finalized, broken down by age bracket (e.g., 30-40, 40-50).

--So like the previous query, I need the Sum Insured but this time it is not just avergae.
--I need to find the sum insured requested vs sum insured finalized and then break it down by age. 
--Beaking down by age is not a task because I can join the final to client table which has dob to calculate the age.
--I need to see think where sum insured requested is and where final is.
--The final might be in factsales activity where sale=1 because that means they agreed at that price and made the sale.
--The initial sum insured table is where ?
--Lets do some searching

-- Ask devashish what does benefit sum insured mean ? How is it different from sum insured ? And why is there no benefit sum insured for sales > 0 ? I mean how does that make sense that there is a benefit sum insured even when there is no sale ?
--1 policy can have multiple benefits for example life insurance has x benefit for death and y benefit for y.
--Leave benefit sum insured for now because they shouldn't be in fact sales activity.

select distinct ProductCode
from hollarddw.dbo.FactUnderwriting
-- All products having underwriting

--For the non underwritten products Have to see.

--Saw many tables but couldn't see sum insured initial one
--I should see the table which records the first conversation between the agent and the customer. That would have the initial sum insured value.
--According to chatgpt maybe benefit sum insured or the recommended benefit sum insured shows the initial sum insured. I will confirm with Devashish.
--Will write the final sum insured based on the sum insured column.
--How come sale  is 0 but sum insured > 0 ? --> Ignore them. Also many products are closed from past years so add isactive=1


WITH ClientAgeData AS (
    SELECT 
        fs.ClientID,
        cl.DOB,
        evolve.dbo.fn_AgeLastBirthday(cl.DOB, GETDATE()) AS Age,
        fs.RecommendedBenefitSumInsured,
        fs.BenefitSumInsured,
		fs.SumInsured
    FROM [HollardDW].[dbo].[FactSalesActivity] fs
    LEFT JOIN [HollardDW].[dbo].[DimClient] cl
        ON fs.ClientID = cl.ClientID
    WHERE cl.DOB IS NOT NULL
)

, AgeBracketed AS (
    SELECT *,
        CASE 
            WHEN Age BETWEEN 30 AND 39 THEN '30-39'
            WHEN Age BETWEEN 40 AND 49 THEN '40-49'
            WHEN Age BETWEEN 50 AND 59 THEN '50-59'
            WHEN Age BETWEEN 60 AND 69 THEN '60-69'
            WHEN Age BETWEEN 70 AND 79 THEN '70-79'
            ELSE 'Other'
        END AS AgeBracket
    FROM ClientAgeData
)

SELECT 
    AgeBracket,
    COUNT(DISTINCT ClientID) AS ClientCount,
    AVG(CAST(RecommendedBenefitSumInsured AS FLOAT)) AS Avg_Recommended_Benefit_SumInsured,
    AVG(CAST(BenefitSumInsured AS FLOAT)) AS Avg_Benefit_SumInsured,
	AVG(CAST(SumInsured AS FLOAT)) AS Avg_SumInsured
FROM AgeBracketed
WHERE AgeBracket != 'Other'
GROUP BY AgeBracket
ORDER BY AgeBracket;


select distinct productcode from [HollardDW].[dbo].[FactSalesActivity] where sales = 0 and suminsured>0 and quotes =0

select * from evolve.dbo.tblproduct where productcode in ('API','GPI','PPI','HPI','RPI')


