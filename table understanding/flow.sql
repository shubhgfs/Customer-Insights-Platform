-- Campaign
--  Select * from evolve.dbo.tblCampaign
--  where brandid = 1
--  order by 5 desc

 
-- -- Each campaign have multiple batch
-- SELECT *
--   FROM evolve.dbo.[tblCampaignBatch]
--   where CampaignID=4398
--   and campaignbatchid=152252

-- There are multiple campaigns (evolve.dbo.tblCampaign) and each campaign has multiple campaign batch Id
-- Each campaign batch consists of a n number of leads which are uploaded accordig to the dtmloaded date.
-- Since everyday new leads come in due to these campaigns, there are multiple batches.

-- Each row in evolve.[dbo].[tblCampaignQueue] has the clientid which is involved in that particular campaign batchid.
-- So we know that these clientids are the leads for the journey for that campaign.

-- For example the (select * from evolve.[dbo].[tblCampaignQueue] where CampaignBatchID = 152252) has 443 rows meaning there are 443 clients in this batch of the campaign.

-- So we want to track all these leads and see that how many received a quote in the journey and further converted to a sale.
-- Right now there is an algo GNWI which takes these leads (clientids from campaign batch) and ranks them according to priority and assigns to the relevant agent.

-- So we need the dataset to track this.

-- So we would need to track the client at each step.
-- Assuming there is 1 clientid in 1 batch.

-- We would need, that for each campaign batch have the clientid their batch loading date, deactivate date, first contact date, quote date, sale date if those are there. 
-- So we will also need flags for first attempt, sale, quote.

-- Based on the quote / client id we can have the demographics and other application underwriting question set.

-- The granularity should be each clientid in each campaign batch.

-- Can use the dtm actiavte to track all the leads for the campaign. 
-- Seeing all the leads who made a sale between dtmactivate and dtmdeactivate + 30 (variable)

-- See all the campaigns for which real life has made a sale for 2025.

-- Each batch have multiple CIDS i.e multiple leads

-- select * from evolve.[dbo].[tblCampaignQueue]
-- where CampaignBatchID = 152252

-- CCMS 
-- select * from evolve.dbo.tblCCMSCallLogCTI
-- where ClientId in (
-- select ClientId from evolve.dbo.tblCampaignQueueHistory			-- take a union tblcampaignqueue and tblcampaignqueuehistory
-- where CampaignBatchID = 152252
-- )

-- CID --> CCMS --> APPLICATION --> QUOTE

-- select *
-- from evolve.dbo.tblClient c
-- left join evolve.dbo.tblapplication app
-- on app.ClientId=c.ClientID
-- left join evolve.dbo.tblQuote q
-- on app.QuoteId=q.QuoteID
-- where c.ClientId in (
-- select ClientId from evolve.[dbo].[tblCampaignQueueHistory]
-- where CampaignBatchID = 152252
-- )
-- and q.clientpolicynumber is not null




-- select * from hollarddw.dbo.factsalesactivity where clientid in (select distinct c.clientid
-- from evolve.dbo.tblClient c
-- left join evolve.dbo.tblapplication app
-- on app.ClientId=c.ClientID
-- left join evolve.dbo.tblQuote q
-- on app.QuoteId=q.QuoteID
-- where c.ClientId in (
-- select ClientId from evolve.[dbo].[tblCampaignQueueHistory]
-- where CampaignBatchID = 152252
-- )
-- and sales > 0
-- )

drop table if exists #tmp
select dateid, clientid, clientsourceid, s.SourceCategory, s.SourceSubCategory
into #tmp
from hollarddw.dbo.factsalesactivity fs
left join [HollardDW].[dbo].[DimSource] s
on fs.clientsourceid=s.sourceid
-- where sales > 0
and dateid >= '2025-01-01'
and fs.brandid=1
and fs.producttypeid=1
and fs.sourcesystemid = 1
and s.BrandName = 'Real'
and s.ProductType = 'Life'



-- select * from evolve.dbo.tblsource


-- select * from evolve.dbo.tblclient


-- select 
--     s.SourceCategory, 
--     s.SourceSubCategory, 
--     count(distinct fs.clientid) as ClientCount
-- from hollarddw.dbo.factsalesactivity fs
-- left join hollarddw.dbo.DimSource s
--     on fs.clientsourceid = s.sourceid
-- where fs.sales > 0
--     and fs.dateid >= '2025-01-01'
--     and fs.brandid = 1
--     and fs.producttypeid = 1
--     and fs.sourcesystemid = 1
-- 	and s.BrandName = 'Real'
-- 	and s.ProductType = 'Life'
-- group by s.SourceCategory, s.SourceSubCategory
-- order by ClientCount desc

select * from #tmp



select 
    SourceCategory, 
    SourceSubCategory, 
    count(distinct clientid) as ClientCount
from #tmp t
group by SourceCategory, SourceSubCategory
order by ClientCount desc


-- select * from evolve.dbo.tblclient cl
-- where brandid=1
-- and dtmLastUpdated>='2025-01-01'
-- and islead=1


-- select * from evolve.dbo.tblquote
-- where dtminserted >= '2025-01-01'


-- select * from evolve.dbo.tblapplication
-- where dtminserted >= '2025-01-01'


-- select s.SourceCategory, 
--     s.SourceSubCategory,  count(*) as countt from [Evolve].[dbo].[tblClientLead] fs
-- left join hollarddw.dbo.DimSource s
--     on fs.sourceid = s.sourceid
-- where dtminserted >= '2024-12-01' and dtminserted < '2025-05-01'
-- and s.BrandName = 'Real'
-- and s.ProductType = 'Life'
-- group by s.SourceCategory, s.SourceSubCategory
-- order by countt desc 



drop table if exists #tmp2
select fs.*, s.SourceCategory, 
    s.SourceSubCategory into #tmp2 from [Evolve].[dbo].[tblClientLead] fs
left join hollarddw.dbo.DimSource s
    on fs.sourceid = s.sourceid
where dtminserted >= '2024-12-01' and dtminserted < '2025-05-01'
and s.BrandName = 'Real'
and s.ProductType = 'Life'


select SourceCategory, 
    SourceSubCategory,  count(*) as countt from #tmp2 tt
group by SourceCategory, SourceSubCategory
order by countt desc 





-- Step 1: Create a table for all leads for Real Life from Jan to April 2025
drop table if exists #AllLeads;
select 
    cl.ClientID,
    cl.dtmInserted as LeadDate,
    s.SourceCategory,
    s.SourceSubCategory
into #AllLeads
from [Evolve].[dbo].[tblClientLead] cl
left join hollarddw.dbo.DimSource s
    on cl.sourceid = s.sourceid
where cl.dtmInserted >= '2025-01-01' 
  and cl.dtmInserted < '2025-05-01'
  and s.BrandName = 'Real'
  and s.ProductType = 'Life';

-- Step 2: Capture call activity for each lead
drop table if exists #CallActivity;
select 
    al.ClientID,
    al.LeadDate,
    count(cl.CallID) as NumberOfCalls,
    min(cl.dtmInserted) as FirstCallDate,
    max(cl.dtmInserted) as LastCallDate,
    al.SourceCategory,
    al.SourceSubCategory
into #CallActivity
from #AllLeads al
left join evolve.dbo.tblCCMSCallLogCTI cl
    on al.ClientID = cl.ClientID
    and cl.dtmInserted >= al.LeadDate -- Ensure call happens after the lead date
    and cl.dtmInserted < dateadd(day, 30, al.LeadDate) -- Calls within 30 days of lead date
group by 
    al.ClientID, al.LeadDate, al.SourceCategory, al.SourceSubCategory;

-- Step 3: Add a flag for Sale or No Sale
drop table if exists #LeadsWithSales;
select 
    ca.ClientID,
    ca.LeadDate,
    ca.NumberOfCalls,
    ca.FirstCallDate,
    ca.LastCallDate,
    fs.SaleDateTimeID as SaleDate,
    ca.SourceCategory,
    ca.SourceSubCategory,
    case 
        when fs.ClientID is not null then 'Sale'
        else 'No Sale'
    end as SaleFlag
into #LeadsWithSales
from #CallActivity ca
left join hollarddw.dbo.factsalesactivity fs
    on ca.ClientID = fs.ClientID
    and fs.SaleDateTimeID between ca.LeadDate and dateadd(day, 30, ca.LeadDate)
    and fs.sales > 0
    and fs.brandid = 1
    and fs.producttypeid = 1
    and fs.sourcesystemid = 1
    and fs.dateid >= '2025-01-01';

-- Step 4: Final query to capture the journey
drop table if exists #Final1;
select 
    lw.ClientID,
	lw.SourceCategory,
	lw.SourceSubCategory,
    lw.LeadDate,
    lw.NumberOfCalls,
    lw.FirstCallDate,
    lw.LastCallDate,
    lw.SaleFlag,
    lw.SaleDate
into #Final1
from #LeadsWithSales lw
order by lw.LeadDate, lw.ClientID;



select count(*) from #final1 where leaddate >= '2025-02-01' and leaddate < '2025-03-01'
select count(distinct clientid) from #final1 where numberofcalls > 0 and leaddate >= '2025-02-01' and leaddate < '2025-03-01'
select count(distinct clientid) from #final1 where saleflag='Sale' and leaddate >= '2025-02-01' and leaddate < '2025-03-01'



