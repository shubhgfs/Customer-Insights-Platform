-- Hello Shubh,

-- Below are the Reharvest extraction rules:

-- • From Web leads table: vwWebLeadWithHistory
-- • Client created in between -30 days to maximum 12 months from the extraction date;
-- • Client status is closed, tblClient
-- • Client is in the eligibility age range for the product;
-- • Has no call log in the last 21 days, tblCallLog
-- • Is run ONCE post any new web lead received for the client (ensure we only send the customer once for the LN activity per web lead received);
-- • Does not have a sale or an application was Declined /RUW Declined;
-- • Not in internal DNC, tblClientCommunicationUnsubscription
-- • lead closed reason is not due to any of these (DO NOT CALL REGISTER - Explicit, Deceased or Non-English speaking), tblClosedReason
-- • Kickbox wash and any other invalid email address wash;
-- • For Funeral: the age eligibility is in between 40-79

-- Please try to cross reference with the current reharvest script to see if any filters are missing. 

-- Thanks,



-- Step 1: Drop existing temp tables
IF OBJECT_ID('tempdb..#tmpWeb') IS NOT NULL DROP TABLE #tmpWeb;


-- Step 2: Extract eligible web leads
SELECT wl.*
INTO #tmpWeb
FROM (select *, ROW_NUMBER() over (	partition by email, ClientBrandID
									order by ProductTypeid asc, dtminserted desc) rn
		from Evolve.dbo.vwWebLeadWithHistory 
		where workitemstatusid <> 1
		and dtmInserted BETWEEN DATEADD(MONTH, -12, GETDATE()) AND DATEADD(DAY, -30, GETDATE())
		and clientid is not null
		and duplicatewebleadid is null
		AND Email IS NOT NULL
		AND Email NOT LIKE '%greenstone%' 
		AND Email NOT LIKE '%test%' 
		AND Email LIKE '%@%'
		and clientbrandid in (0,1)
		and producttypeid = 1) wl  ---- Closed Leads
LEFT JOIN Evolve.dbo.tblClient c 
    ON wl.ClientID = c.ClientID 
LEFT JOIN (
    SELECT DISTINCT ClientID 
    FROM Evolve.dbo.tblCallLog 
    WHERE DATEDIFF(DAY, dtmInserted, GETDATE()) <= 21
) cl 
    ON wl.ClientID = cl.ClientID 
--LEFT JOIN HollardDW.dbo.FactSalesActivity fs 
--    ON wl.ClientID = fs.ClientID
LEFT JOIN (select * from HollardDW.dbo.FactUWAction where UWAppStatus in ('Declined', 'RUW - Decline', 'Sale')) fa 
    ON wl.ClientID = fa.ClientID
WHERE 1=1
	AND c.StatusID = 4 -- Client is Closed
 --   AND Evolve.dbo.fn_AgeLastBirthday(c.DOB, GETDATE()) BETWEEN 40 AND 79 -- Funeral age check
    AND cl.ClientID IS NULL -- No call log in past 21 days
    --AND fs.Sales = 0  -- No sale
	AND fa.ClientID IS NULL -- Not a sale or Declined
and rn =1

alter table #tmpWeb drop column rn


select  webleadtypeid, count(*)
from #tmpWeb
group by webleadtypeid


select  email, clientbrandid, count(*)
from #tmpWeb
group by email, clientbrandid
having count(*) > 1

select  *
from #tmpWeb
where webleadid in ('35063483', '35063492')

select  *
from #tmpWeb
order by email, rn

--select *
--from #tmpWeb
--where email <> emailaddress

IF OBJECT_ID('tempdb..#tmpFiltered') IS NOT NULL DROP TABLE #tmpFiltered;
-- Step 3: Filter against DNC, unsubscribed, invalid emails, closed reasons
SELECT wl.*
INTO #tmpFiltered
FROM #tmpWeb wl
LEFT JOIN EvolveKPI.dbo.loyaltyemailstatus les 
    ON wl.Email = les.Email
LEFT JOIN (
    SELECT DISTINCT Email 
    FROM EvolveKPI.dbo.vwEmailUnsubs 
    WHERE Email IS NOT NULL
) unsubs 
    ON wl.Email = unsubs.Email
--LEFT JOIN Evolve.dbo.tblClientCommunicationUnsubscription dnc 
--    ON wl.ClientID = dnc.ClientID
LEFT JOIN (
    SELECT DISTINCT ClientID 
    FROM Evolve.dbo.tblClosedLeads 
    WHERE ReasonID IN (8, 9, 15) -- DO NOT CALL REGISTER - Explicit, Deceased, Non-English speaking
) closed_reasons 
    ON wl.ClientID = closed_reasons.ClientID
WHERE 
    -- Email validation and Kickbox wash
    ISNULL(
        CASE 
            WHEN wl.Email LIKE '%greenstone.com%' THEN 'invalid'
            WHEN wl.Email LIKE '%greentone.com%' THEN 'invalid'
            WHEN wl.Email LIKE '%hfs.com.au%' THEN 'invalid'
            WHEN wl.Email LIKE '%real.com.au%' THEN 'invalid'
            WHEN wl.Email LIKE '%clientemail@pt.qld.gov.au%' THEN 'invalid'
            WHEN wl.Email LIKE '%noemail@%' THEN 'invalid'
            WHEN wl.Email LIKE '%nil@nil.com%' THEN 'invalid'
            WHEN LEN(ISNULL(wl.Email, '')) > 3 
                 AND wl.Email LIKE '%@%' 
                 AND LTRIM(RTRIM(wl.Email)) NOT LIKE '% %' 
                 AND les.Email IS NOT NULL 
            THEN les.[Status]
            ELSE 'unknown'
        END, 'unknown'
    ) IN ('deliverable', 'risky', 'unknown')
    AND unsubs.Email IS NULL
    --AND dnc.ClientID IS NULL
    AND closed_reasons.ClientID IS NULL


-- Step 4: "Run Once" filter using master table
-- Assume you maintain: dbo.MasterReharvestSent (ClientID, WebLeadID, ProcessedDate, etc.)

SELECT ln.*
FROM #tmpFiltered ln
left join EvolveKPI.dbo.tblnurturingMasterG4 excl
		on ln.Email=excl.email and ln.BrandID=excl.brandID and case when excl.ProductType = 'Life' then 'ALife' else excl.ProductType end <= ln.ProductType and excl.nurturingGroupID in (40) --Ensures Life is not overidden
WHERE excl.ClientID IS NULL
;




    