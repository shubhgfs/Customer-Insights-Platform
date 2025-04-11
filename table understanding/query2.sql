-- SQL Query to Find When Non-Converting Customers Left
-- Here's a SQL query that identifies at which call customers who received a quote but didn't make a purchase left the sales process:

-- What This Query Does
-- First identifies all client-quote combinations and whether each resulted in a sale
-- Filters to only include quotes that didn't convert to a sale
-- Finds all calls made to these clients after they received their quote
-- Counts how many calls each client received before they "left" (didn't proceed to purchase)
-- Groups the results to show how many customers dropped off after each call number
-- The results will show you a distribution like:

-- X customers left after receiving no calls following their quote
-- Y customers left after 1 call
-- Z customers left after 2 calls
-- And so on
-- This will help you identify at which point in the calling sequence most customers are abandoning the sales process.

WITH QuoteActivity AS (
    -- Get quote activity and identify if a sale was made for each client-quote combination
    SELECT 
        ClientID,
        QuoteID,
        MIN(DateID) AS FirstQuoteDate,
        MAX(CASE WHEN Sales = 1 THEN 1 ELSE 0 END) AS MadePurchase
    FROM [HollardDW].[dbo].[FactSalesActivity]
    GROUP BY ClientID, QuoteID
),
NonPurchasingQuotes AS (
    -- Select only clients who received quotes but didn't make a purchase
    SELECT 
        ClientID,
        QuoteID,
        FirstQuoteDate
    FROM QuoteActivity
    WHERE MadePurchase = 0
),
ClientCalls AS (
    -- Get all calls for these non-purchasing clients after their quote date
    SELECT 
        cl.ClientId,
        npq.QuoteID,
        cl.DateID AS CallDate,
        cl.CallType,
        cl.CallOutcome,
        ROW_NUMBER() OVER (PARTITION BY cl.ClientId, npq.QuoteID ORDER BY cl.DateID, cl.CallId) AS CallSequence
    FROM [HollardDW].[dbo].[FactCCMSCallLogCTI] cl
    JOIN NonPurchasingQuotes npq ON cl.ClientId = npq.ClientID
    WHERE cl.DateID >= npq.FirstQuoteDate -- Only include calls after the quote was given
),
QuoteCallCounts AS (
    -- Count the maximum call sequence for each non-purchasing quote
    SELECT 
        npq.ClientID,
        npq.QuoteID,
        ISNULL(MAX(cc.CallSequence), 0) AS TotalCallsAfterQuote
    FROM NonPurchasingQuotes npq
    LEFT JOIN ClientCalls cc ON npq.ClientID = cc.ClientId AND npq.QuoteID = cc.QuoteID
    GROUP BY npq.ClientID, npq.QuoteID
)
-- Final result: Distribution of when customers left the process
SELECT 
    CASE
        WHEN TotalCallsAfterQuote = 0 THEN 'No calls after quote'
        ELSE CAST(TotalCallsAfterQuote AS VARCHAR) + ' call(s)'
    END AS LeftAfterCallNumber,
    COUNT(*) AS NumberOfCustomers,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(5,2)) AS PercentageOfTotal
FROM QuoteCallCounts
GROUP BY TotalCallsAfterQuote
ORDER BY TotalCallsAfterQuote;