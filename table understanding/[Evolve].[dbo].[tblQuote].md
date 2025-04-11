# [Evolve].[dbo].[tblQuote]

```sql
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [QuoteID]
      ,[ProductCode]
      ,[CoverTypeID]
      ,[TotalPremium]
      ,[TotalRealBonus]
      ,[dtmInserted]
      ,[dtmExpiry]
      ,[PaymentFrequencyID]
      ,[PaymentMethodID]
      ,[FirstCollectionDay]
      ,[BankCode]
      ,[BSBNo]
      ,[BranchName]
      ,[AccountHolderName]
      ,[CreditCardTypeID]
      ,[CCNoEncryted]
      ,[CCExpiry]
      ,[AccountTypeID]
      ,[CCVerificationNo]
      ,[CCNameOnCard]
      ,[BatchTransferID]
      ,[dtmSaleCompleted]
      ,[AccountNumberOriginal]
      ,[CCNoOriginal]
      ,[AccountNumber]
      ,[CCNo]
      ,[UWVersion]
      ,[InceptionEv]
      ,[dtmSaleReversed]
      ,[ChannelID]
      ,[SourceID]
      ,[IsLocked]
      ,[CCTokenNumber]
      ,[IsUpdatedFromLatestDisclosure]
      ,[NPV_Gross_HFS_Comm]
      ,[NPV_Insurer_Upfront]
      ,[NPV_Insurer_Trail]
      ,[NPV_Partner_Upfront]
      ,[NPV_Partner_Trail]
      ,[NPV_SalesIncentive_Upfront]
      ,[NPV_SalesIncentive_Trail]
      ,[NPV_RealLiability]
      ,[CommissionCode]
      ,[CDN]
      ,[WebsiteID]
      ,[ClientMemberTypeID]
      ,[SoldBy]
      ,[UpdatedBy]
      ,[UpdatedDate]
      ,[IncomeLevelId]
      ,[JointIncomeLevelId]
      ,[PolicyStatusId]
      ,[dtmPaymentCycleStart]
      ,[dtmNextCollection]
      ,[dtmSubsequentCollection]
      ,[dtmPolicyTermination]
      ,[PolicyTerminationReason]
      ,[CPIStatusId]
      ,[dtmRenewal]
      ,[PolicyTerminationReasonId]
      ,[ToBeReInstated]
      ,[OldClientPolicyNumber]
      ,[NextCollectionDay]
      ,[ClientPolicyNumber]
      ,[dtmUpdated]
      ,[PartnerAgentID]
      ,[PolicyRegisteredState]
      ,[LockedBy]
      ,[WorkItemID]
      ,[dtmNoEndorsementTill]
      ,[AtSalePaymentFrequencyID]
      ,[IsHighValuePolicy]
      ,[IsTransactionInFlight]
      ,[IsStp]
      ,[IsIncStpActioned]
      ,[FinancialInstitutionNumber]
      ,[TransitNumber]
      ,[PaymentProviderCustomerID]
      ,[PaymentProviderPaymentMethodID]
  FROM [Evolve].[dbo].[tblQuote]
```

## Column Descriptions

| Column Name | Description |
|-------------|-------------|
| QuoteID | Primary key identifier for each quote record |
| ProductCode | Code representing the insurance product type (e.g., HFI, RFE, RFL) |
| CoverTypeID | Type of insurance coverage (1 = Individual, 2 = Joint/Family) |
| TotalPremium | Total premium amount charged to the customer |
| TotalRealBonus | Bonus amount associated with the policy |
| dtmInserted | Date and time when the quote was created in the system |
| dtmExpiry | Expiration date of the quote |
| PaymentFrequencyID | Frequency of premium payments (F = Fortnightly, M = Monthly, A = Annual) |
| PaymentMethodID | Method of payment (1 = Credit Card, 2 = Direct Debit/Bank Account, 3 = Other) |
| FirstCollectionDay | Date of the first payment collection |
| BankCode | Code identifying the customer's bank |
| BSBNo | Bank-State-Branch number for Australian bank accounts |
| BranchName | Name of the bank branch |
| AccountHolderName | Name of the account holder for payment collection |
| CreditCardTypeID | Type of credit card used for payment |
| CCNoEncryted | Encrypted credit card number |
| CCExpiry | Credit card expiration date |
| AccountTypeID | Type of bank account (e.g., 1 = Savings) |
| CCVerificationNo | Credit card verification code/CVV |
| CCNameOnCard | Name printed on the credit card |
| BatchTransferID | ID for batch payment processing |
| dtmSaleCompleted | Date and time when the sale was completed |
| AccountNumberOriginal | Original account number (before encryption) |
| CCNoOriginal | Original credit card number (before encryption) |
| AccountNumber | Encrypted account number for bank payment |
| CCNo | Encrypted credit card number |
| UWVersion | Underwriting version used for the quote |
| InceptionEv | Event marking the inception of the policy |
| dtmSaleReversed | Date and time when a sale was reversed/cancelled |
| ChannelID | Sales channel identifier (1 = Direct, 2 = Partner, 3 = Other) |
| SourceID | Source of the lead/sale |
| IsLocked | Flag indicating if the quote is locked for editing |
| CCTokenNumber | Token used for secure credit card processing |
| IsUpdatedFromLatestDisclosure | Flag indicating if the policy reflects the latest disclosure update |
| NPV_Gross_HFS_Comm | Net Present Value of gross commission |
| NPV_Insurer_Upfront | Net Present Value of upfront payment to insurer |
| NPV_Insurer_Trail | Net Present Value of trail commission to insurer |
| NPV_Partner_Upfront | Net Present Value of upfront payment to partner |
| NPV_Partner_Trail | Net Present Value of trail commission to partner |
| NPV_SalesIncentive_Upfront | Net Present Value of upfront sales incentive |
| NPV_SalesIncentive_Trail | Net Present Value of trail sales incentive |
| NPV_RealLiability | Net Present Value of real liability |
| CommissionCode | Code representing the commission structure |
| CDN | Customer Delivery Network identifier |
| WebsiteID | Identifier for the website where the quote originated |
| ClientMemberTypeID | Type of client membership |
| SoldBy | User ID of the agent who made the sale |
| UpdatedBy | User ID of the person who last updated the record |
| UpdatedDate | Date when the record was last updated |
| IncomeLevelId | Income bracket of the primary policyholder |
| JointIncomeLevelId | Income bracket of the joint policyholder (if applicable) |
| PolicyStatusId | Current status of the policy (e.g., Active, Lapsed, Cancelled) |
| dtmPaymentCycleStart | Start date of the payment cycle |
| dtmNextCollection | Date of the next scheduled payment collection |
| dtmSubsequentCollection | Date of the collection after the next one |
| dtmPolicyTermination | Date when the policy was/will be terminated |
| PolicyTerminationReason | Text description of why the policy was terminated |
| CPIStatusId | Consumer Price Index status identifier |
| dtmRenewal | Date when the policy is scheduled for renewal |
| PolicyTerminationReasonId | ID code for the termination reason |
| ToBeReInstated | Flag indicating if the policy should be reinstated |
| OldClientPolicyNumber | Previous policy number if this is a renewal/replacement |
| NextCollectionDay | Day of month/week for the next collection |
| ClientPolicyNumber | Policy number assigned to the client |
| dtmUpdated | Date and time of the last record update |
| PartnerAgentID | ID of the partner agent associated with the policy |
| PolicyRegisteredState | Australian state or territory where the policy is registered |
| LockedBy | User ID of person who has locked the record |
| WorkItemID | Identifier for associated workflow item |
| dtmNoEndorsementTill | Date until which no policy endorsements are allowed |
| AtSalePaymentFrequencyID | Payment frequency set at the time of sale |
| IsHighValuePolicy | Flag indicating if the policy is considered high-value |
| IsTransactionInFlight | Flag indicating if a transaction is currently being processed |
| IsStp | Flag for Straight Through Processing eligibility |
| IsIncStpActioned | Flag indicating if STP has been actioned |
| FinancialInstitutionNumber | ID number of the financial institution |
| TransitNumber | Transit number for Canadian bank accounts |
| PaymentProviderCustomerID | Customer ID with the payment provider |
| PaymentProviderPaymentMethodID | Payment method ID with the payment provider |

## Sample Data

| QuoteID | ProductCode | CoverTypeID | TotalPremium | TotalRealBonus | dtmInserted | dtmExpiry | PaymentFrequencyID | PaymentMethodID | FirstCollectionDay | BankCode | BSBNo | BranchName | AccountHolderName | CreditCardTypeID | CCNoEncryted | CCExpiry | AccountTypeID | CCVerificationNo | CCNameOnCard | BatchTransferID | dtmSaleCompleted | AccountNumberOriginal | CCNoOriginal | AccountNumber | CCNo | UWVersion | InceptionEv | dtmSaleReversed | ChannelID | SourceID | IsLocked | CCTokenNumber | IsUpdatedFromLatestDisclosure | NPV_Gross_HFS_Comm | NPV_Insurer_Upfront | NPV_Insurer_Trail | NPV_Partner_Upfront | NPV_Partner_Trail | NPV_SalesIncentive_Upfront | NPV_SalesIncentive_Trail | NPV_RealLiability | CommissionCode | CDN | WebsiteID | ClientMemberTypeID | SoldBy | UpdatedBy | UpdatedDate | IncomeLevelId | JointIncomeLevelId | PolicyStatusId | dtmPaymentCycleStart | dtmNextCollection | dtmSubsequentCollection | dtmPolicyTermination | PolicyTerminationReason | CPIStatusId | dtmRenewal | PolicyTerminationReasonId | ToBeReInstated | OldClientPolicyNumber | NextCollectionDay | ClientPolicyNumber | dtmUpdated | PartnerAgentID | PolicyRegisteredState | LockedBy | WorkItemID | dtmNoEndorsementTill | AtSalePaymentFrequencyID | IsHighValuePolicy | IsTransactionInFlight | IsStp | IsIncStpActioned | FinancialInstitutionNumber | TransitNumber | PaymentProviderCustomerID | PaymentProviderPaymentMethodID |
|---------|------------|-------------|--------------|----------------|-------------|-----------|-------------------|-----------------|-------------------|----------|--------|------------|-------------------|-----------------|-------------|----------|--------------|-----------------|--------------|----------------|-----------------|----------------------|--------------|--------------|------|-----------|------------|----------------|-----------|----------|----------|--------------|--------------------------------|-------------------|---------------------|------------------|-------------------|------------------|---------------------------|--------------------------|-------------------|---------------|-----|-----------|-------------------|--------|-----------|------------|--------------|-------------------|---------------|---------------------|-------------------|------------------------|---------------------|------------------------|------------|-----------|--------------------------|---------------|----------------------|-------------------|-------------------|------------|---------------|----------------------|----------|-----------|----------------------|--------------------------|------------------|----------------------|-------|------------------|--------------------------|--------------|--------------------------|------------------------------|
| 1 | HFI | 1 | 0.00 | NULL | 2018-12-11 21:07:00 | 2018-12-12 00:00:00 | F | 2 | 2050-01-01 00:00:00 | 3 | 012345 | Mascot | John Smith | NULL | NULL | 12-30 | 1 | NULL | NULL | 1000001474 | 2018-09-08 00:00:00.000 | NULL | NULL | 0x02000000CA9716748C78EC7443EF5E59B6E7A7CABA9A7FA11DBC897A3310B90CBE85A05EB01002214A0BA55AE76AC8621C599F37 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |  | NULL | NULL | 1 | jamesw02 | NULL | NULL | NULL | NULL | 61 | 2050-01-01 00:00:00 | 2050-01-01 00:00:00 | 2070-01-01 00:00:00 | 2024-11-16 00:00:00 | NULL | 1 | 2050-01-01 00:00:00 | 14 | NULL | NULL | NULL | 100000000 | 2024-11-16 10:56:43.160 | NULL | NSW | NULL | NULL | NULL | NULL | NULL | 1 | NULL | NULL | NULL | NULL | NULL | NULL |
| 33 | RFE | 2 | 10.05 | 82.34 | 2008-06-10 09:46:00 | 2008-06-10 09:46:00 | F | 2 | 2008-06-16 00:00:00 | 9 | 633000 | 633000 | Aleisha Mason | NULL | NULL | NULL | 1 | NULL | NULL | 1000 | 2008-06-10 15:55:00.000 | åÐ­$rLz¼ | NULL | 0x010000004F9D320B36056ED1C904B2E9DC860BE2A62282308B16ED1AC25FAB1752A8FDE0 | NULL | 204 | NULL | NULL | 1 | 12 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 1 | kerrih02 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 10 | NULL | F | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 36 | RFE | 1 | 4.3307 | 1.4581 | 2008-06-10 09:47:00 | 2008-06-10 09:47:00 | F | 2 | 2008-06-13 00:00:00 | 9 | 633000 | 633000 | Barry Busby | NULL | NULL | NULL | 1 | NULL | NULL | 1000 | 2008-06-10 16:02:00.000 | å»£²j'Tß´ | NULL | 0x0100000026816B6A6C68E19AF1C160C3485763009759387FF4CF6CC1D4DC09DBE5D3B864 | NULL | 204 | NULL | NULL | 1 | 95 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 1 | jacquw01 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 10 | NULL | F | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 37 | RFL | 2 | 93.16 | 832.20 | 2008-06-10 09:48:00 | 2008-06-10 09:48:00 | F | 2 | 2008-06-23 00:00:00 | 18 | 484799 | 484799 | Anne Scott | NULL | NULL | NULL | 1 | NULL | NULL | 1000 | 2008-06-11 15:56:00.000 | ¡–hvÐ P | NULL | 0x01000000058B13FE4F59FFC9B8B5664F0978BBCA30A6EF36C406AF410C5E864B1FA0330A | NULL | 204 | NULL | NULL | 1 | 106 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 1 | josepb01 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 10 | NULL | F | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 41 | RFL | 2 | 21.3076 | 6.7172 | 2008-06-10 09:56:00 | 2008-06-10 09:56:00 | F | 2 | 2008-06-23 00:00:00 | 9 | 633000 | 633000 | Aleisha Mason | NULL | NULL | NULL | 1 | NULL | NULL | 1000 | NULL | åÐ­$rLz¼ | NULL | 0x01000000DCE68759C2DAF0B4CF602183A630EDCBE007542D39500254A63C385AEB6152CF | NULL | NULL | NULL | NULL | 1 | 12 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 1 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 10 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 42 | RFE | 1 | 21.3876 | 7.1666 | 2008-06-10 09:57:00 | 2008-06-10 09:57:00 | F | 2 | 2008-07-01 00:00:00 | 19 | 082441 | 082440 | Peter Niland | NULL | NULL | NULL | 1 | NULL | NULL | 1000 | 2008-06-10 15:51:00.000 | 1´yæç | NULL | 0x01000000FE567543FA8637666B6B1C9EBBA687D07A9B09656D473E11E85E30378BCCC38A | NULL | 204 | NULL | NULL | 1 | 12 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 1 | caterc01 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 10 | NULL | F | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |

---

### 🧮 **General Data Overview**
1. **Total number of quotes:**
   ```sql
   SELECT COUNT(*) AS TotalQuotes FROM [Evolve].[dbo].[tblQuote];
   ```
TotalQuotes
13487394

   **Insight:** The database contains over 13.4 million quotes, indicating a substantial volume of insurance quote activity. This large dataset provides a comprehensive view of the customer base and product interest across different time periods.

2. **Number of distinct products sold:**
   ```sql
   SELECT COUNT(DISTINCT ProductCode) AS DistinctProducts FROM [Evolve].[dbo].[tblQuote];
   ```
DistinctProducts
102

   **Insight:** With 102 distinct product codes, the company maintains a diverse portfolio of insurance products. This diversification strategy allows them to cater to various customer segments and risk profiles while potentially reducing overall portfolio risk through product variety.

3. **Quotes with a completed sale:**
   ```sql
   SELECT COUNT(*) AS CompletedSales FROM [Evolve].[dbo].[tblQuote]
   WHERE dtmSaleCompleted IS NOT NULL;
   ```
CompletedSales
1420624

   **Insight:** Only approximately 10.5% of quotes (1.42 million out of 13.48 million) resulted in completed sales, indicating a conversion rate that presents significant opportunity for improvement. Understanding why nearly 90% of quotes don't convert to sales could reveal valuable insights for improving sales processes and product offerings.

---

### 💸 **Premium and Bonus Insights**
4. **Average total premium across all quotes:**
   ```sql
   SELECT AVG(TotalPremium) AS AvgTotalPremium FROM [Evolve].[dbo].[tblQuote];
   ```
AvgTotalPremium
77.0312

   **Insight:** The average premium of $77.03 across all quotes provides a baseline for pricing strategy. This figure should be evaluated alongside customer demographics, policy types, and coverage amounts to identify optimal price points for different customer segments and products.

5. **Total real bonus distributed:**
   ```sql
   SELECT SUM(TotalRealBonus) AS TotalBonus FROM [Evolve].[dbo].[tblQuote];
   ```
TotalBonus
477887732.0857

   **Insight:** Nearly $478 million in real bonuses have been distributed, highlighting the company's significant investment in customer incentives and loyalty rewards. Analyzing the relationship between these bonuses and customer retention could reveal the effectiveness of the bonus program in maintaining long-term customer relationships.

6. **Distribution of Total Premium by Cover Type:**
   ```sql
   SELECT CoverTypeID, AVG(TotalPremium) AS AvgPremium, COUNT(*) AS CountQuotes
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY CoverTypeID;
   ```
CoverTypeID	AvgPremium	CountQuotes
NULL	94.9716	1678838
1	70.9074	10177767
2	116.9665	1630789

   **Insight:** Cover Type 1 (Individual) represents over 75% of all quotes with an average premium of $70.91, significantly lower than Cover Type 2 (Joint/Family) at $116.97. This premium differential of approximately 65% between individual and family coverage aligns with the expected higher risk exposure for multiple covered individuals. The 1.67 million quotes with NULL cover types at a premium of $94.97 could represent either a data quality issue or specialized products that don't fit the standard categorization.

---

### 🧾 **Payment Behavior**
7. **Distribution of payment methods:**
   ```sql
   SELECT PaymentMethodID, COUNT(*) AS Count
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY PaymentMethodID;
   ```
PaymentMethodID	Count
NULL	11808482
1	560337
2	1092986
3	25589

   **Insight:** Direct Debit/Bank Account payments (ID 2) are nearly twice as popular as Credit Card payments (ID 1), with over 1 million customers choosing bank debits compared to approximately 560,000 opting for credit cards. However, the most concerning finding is that 87.5% of quotes (11.8 million) have no specified payment method, which could indicate incomplete quote processes, system data issues, or quotes abandoned before payment method selection.

8. **Most common payment frequency:**
   ```sql
   SELECT PaymentFrequencyID, COUNT(*) AS Count
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY PaymentFrequencyID
   ORDER BY Count DESC;
   ```
PaymentFrequencyID	Count
F	12504302
M	832365
A	146505
NULL	4222

   **Insight:** Fortnightly payments (F) overwhelmingly dominate the preferred payment frequency at 92.7% of specified frequencies, followed by Monthly (M) at 6.2% and Annual (A) at just 1.1%. This strong preference for fortnightly payments may reflect alignment with common payroll cycles in Australia, helping customers manage their cash flow more effectively.

9. **Quotes with failed or missing payment methods:**
   ```sql
   SELECT COUNT(*) AS MissingPaymentDetails
   FROM [Evolve].[dbo].[tblQuote]
   WHERE PaymentMethodID IS NULL OR PaymentFrequencyID IS NULL;
   ```
MissingPaymentDetails
11808493

   **Insight:** Over 11.8 million quotes (87.5% of total) have missing payment details, closely matching the number with NULL PaymentMethodID. This suggests a systematic issue in the quote process where customers are not reaching the payment details stage, representing a major drop-off point in the customer journey that requires investigation.

---

### 🗓️ **Policy Lifecycle Insights**
10. **Average time from quote to sale (for completed sales):**
   ```sql
   SELECT AVG(DATEDIFF(DAY, dtmInserted, dtmSaleCompleted)) AS AvgDaysToSale
   FROM [Evolve].[dbo].[tblQuote]
   WHERE dtmSaleCompleted IS NOT NULL;
   ```
AvgDaysToSale
0

   **Insight:** The average time from quote creation to sale completion is 0 days, indicating that most sales are completed on the same day the quote is generated. This suggests an efficient sales process where customers who decide to purchase do so immediately, potentially during the same session or call. This immediacy highlights the importance of the initial customer interaction and the need for a seamless quote-to-purchase experience.

11. **Policy expiry and renewal status counts:**
   ```sql
   SELECT 
     COUNT(CASE WHEN dtmExpiry IS NOT NULL THEN 1 END) AS ExpiredQuotes,
     COUNT(CASE WHEN dtmRenewal IS NOT NULL THEN 1 END) AS RenewedQuotes
   FROM [Evolve].[dbo].[tblQuote];
   ```
ExpiredQuotes	RenewedQuotes
12518563	964236

   **Insight:** Of the 12.5 million quotes with expiry dates recorded, only about 7.7% (964,236) have renewal dates assigned. This significant gap between expiry and renewal rates indicates a potential customer retention issue. The fact that most quotes have expiry dates but not renewal dates suggests that many policies are not being renewed upon expiration, representing a substantial opportunity to improve customer retention and lifetime value through more effective renewal strategies.

12. **Quotes that were reversed after sale:**
   ```sql
   SELECT COUNT(*) AS ReversedSales
   FROM [Evolve].[dbo].[tblQuote]
   WHERE dtmSaleReversed IS NOT NULL;
   ```
ReversedSales
8142

   **Insight:** Only 8,142 sales (approximately 0.57% of completed sales) were subsequently reversed, indicating a relatively low cancellation rate for completed policies. This suggests high customer satisfaction with purchased policies or effective underwriting that correctly matches customers with appropriate products. Analyzing the small segment of reversed sales could still yield insights into product issues, misunderstandings during the sales process, or customer service gaps that lead to reversals.

---

### 💼 **Sales Channel & Source Insights**
13. **Sales distribution by channel:**
   ```sql
   SELECT ChannelID, COUNT(*) AS Count
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY ChannelID;
   ```
ChannelID	Count
NULL	3166
1	10122021
2	2269124
3	1093083

   **Insight:** The direct sales channel (ID 1) dominates with over 10.1 million quotes (75.1% of identified channels), followed by partner channels (ID 2) with 2.26 million quotes (16.8%) and other channels (ID 3) with 1.09 million quotes (8.1%). The strong performance of the direct channel suggests effective marketing and direct customer acquisition strategies. However, the higher-than-average volume through partner channels presents opportunities for scaling through strategic partnerships. Only a tiny fraction (0.02%) of quotes lack channel information, indicating good data quality for this field.

15. **Sales per partner agent (top 10):**
   ```sql
   SELECT TOP 10 PartnerAgentID, COUNT(*) AS SalesCount
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY PartnerAgentID
   ORDER BY SalesCount DESC;
   ```
PartnerAgentID	SalesCount
NULL	13470809
7599	226
6756	214
8727	212
6854	208
6809	200
7139	184
8769	178
8881	142
6803	140

   **Insight:** The data shows that 99.9% of quotes (13.47 million) don't have an associated partner agent ID, which indicates either a data quality issue or that most quotes aren't being generated through the partner agent channel. Among identified partner agents, there appears to be a relatively even distribution of quote volume among the top performers, with agent #7599 leading with 226 quotes, followed closely by agents #6756 (214 quotes) and #8727 (212 quotes). The small gap between the top performers suggests a relatively standardized performance among active agents.

---

### 🧮 **Financial Metrics**
16. **Average and total NPV-related fields (insurer and partner):**
   ```sql
   SELECT 
     AVG(NPV_Insurer_Upfront) AS AvgNPVInsurerUpfront,
     AVG(NPV_Partner_Upfront) AS AvgNPVPartnerUpfront,
     SUM(NPV_RealLiability) AS TotalRealLiability
   FROM [Evolve].[dbo].[tblQuote];
   ```
AvgNPVInsurerUpfront	AvgNPVPartnerUpfront	TotalRealLiability
1.38960305034531	0	16387748.6853

   **Insight:** The average Net Present Value (NPV) of upfront payments to insurers is approximately $1.39 per quote, while NPV for partner upfront payments is zero, indicating that the company's commission structure primarily benefits insurers rather than partners in upfront payments. The total real liability NPV of $16.38 million represents the company's estimated total liability in present value terms. This suggests a financial model where the company maintains controlled liability exposure while directing most upfront financial benefits to insurers, potentially as part of a risk management strategy.

17. **Top commission codes by total quotes:**
   ```sql
   SELECT CommissionCode, COUNT(*) AS QuoteCount
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY CommissionCode
   ORDER BY QuoteCount DESC;
   ```
CommissionCode	QuoteCount
NULL	12131532
	763169
A	401597
F	72533
B	62819
G	23326
C	11636
P	7024
V	3432
K	2655
D	2476
E	1203
Q	835
U	815
R	628
I	538
H	427
T	371
J	221
Z	107
Y	30
M	11
L	5
S	4

   **Insight:** Commission code data is missing for 90% of quotes (12.13 million), indicating either a data quality issue or that many quotes don't have commission structures assigned. For quotes with assigned commission codes, code 'A' is most prevalent with 401,597 quotes (29.6% of coded quotes), followed by codes 'F' (72,533) and 'B' (62,819). There are also 763,169 quotes with blank commission codes, which are distinct from NULL values and may represent a specific commission category. This distribution suggests a tiered commission structure where certain codes (likely representing different commission rates or structures) are assigned more frequently than others.

---

### 🔒 **Status and Locking**
18. **How many quotes are locked:**
   ```sql
   SELECT COUNT(*) AS LockedQuotes
   FROM [Evolve].[dbo].[tblQuote]
   WHERE IsLocked = 1;
   ```
LockedQuotes
0

   **Insight:** No quotes are currently locked, which is surprising given the database size. This could indicate either that the locking mechanism isn't being utilized in the system, locks are being properly released after use, or the data might not reflect current system status if this is a snapshot. Proper quote locking is important in multi-user environments to prevent concurrent edits that could lead to data inconsistency.

19. **Number of quotes updated from latest disclosure:**
   ```sql
   SELECT COUNT(*) AS UpdatedFromDisclosure
   FROM [Evolve].[dbo].[tblQuote]
   WHERE IsUpdatedFromLatestDisclosure = 1;
   ```
UpdatedFromDisclosure
684245

   **Insight:** Only 684,245 quotes (5.1% of total) have been updated with the latest disclosure information, suggesting that either the disclosure update process isn't consistently applied across all quotes, or this flag is only relevant for a subset of quotes (possibly those that were active when a disclosure update occurred). Regular disclosure updates are often required for regulatory compliance, so this metric should be monitored to ensure all relevant quotes receive necessary disclosure updates.

---

### 📍 **Geographic or Demographic Info**
20. **Policy registered state distribution:**
   ```sql
   SELECT PolicyRegisteredState, COUNT(*) AS Count
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY PolicyRegisteredState;
   ```
PolicyRegisteredState	Count
NULL	12496638
ACT	13674
NSW	303270
NT	11662
NZ	55613
QLD	227291
SA	62338
TAS	23120
TONGA	1
UK	1
VIC	193633
WA	100153

   **Insight:** Geographic data is missing for 92.7% of quotes (12.49 million), representing a significant data gap that limits geographic analysis. Among quotes with location data, New South Wales (NSW) has the highest representation with 303,270 quotes, followed by Queensland (QLD) with 227,291 and Victoria (VIC) with 193,633. This distribution roughly aligns with Australia's population distribution across states. There are also small numbers of quotes from non-Australian locations (NZ, TONGA, UK), indicating limited international business. The minimal presence in these international markets might represent either targeted expansion efforts or residual policies for customers who moved internationally.

21. **Income level spread:**
   ```sql
   SELECT IncomeLevelId, COUNT(*) AS Count
   FROM [Evolve].[dbo].[tblQuote]
   GROUP BY IncomeLevelId;
   ```
IncomeLevelId	Count
NULL	12864610
1	330531
2	255486
3	13748
4	15561
5	7458

   **Insight:** Income data is missing for 95.4% of quotes (12.86 million), severely limiting income-based customer segmentation. Where income data is available, there's a concentration in the lower income levels, with Level 1 (330,531 quotes) and Level 2 (255,486 quotes) accounting for 86.4% of quotes with income data. The higher income brackets (Levels 3-5) collectively represent only 13.6% of quotes with income data, suggesting either that the company's products primarily appeal to lower-income individuals or that the company's marketing is more effective in reaching these segments.

---

### ⚙️ **Operational / Data Health**
22. **Quotes missing both credit card and bank account details:**
   ```sql
   SELECT COUNT(*) AS IncompletePaymentDetails
   FROM [Evolve].[dbo].[tblQuote]
   WHERE CCNo IS NULL AND AccountNumber IS NULL;
   ```
IncompletePaymentDetails
12310133

   **Insight:** A substantial 91.3% of quotes (12.31 million) lack both credit card and bank account details, aligning with earlier findings about missing payment methods. This confirms a major drop-off in the quote-to-sale funnel before payment details are provided. This could indicate that most quotes are created for price comparison only, customers abandon quotes before completing payment information, or there are issues with the data collection process. Understanding this drop-off point is crucial for improving conversion rates.

23. **Stale quotes that never led to a sale:**
   ```sql
   SELECT COUNT(*) AS StaleQuotes
   FROM [Evolve].[dbo].[tblQuote]
   WHERE dtmSaleCompleted IS NULL AND dtmInserted < DATEADD(MONTH, -6, GETDATE());
   ```
StaleQuotes
11864255

   **Insight:** Nearly 88% of all quotes (11.86 million) are stale, defined as quotes older than 6 months that never converted to sales. This extremely high figure reinforces the low conversion rate identified earlier. These stale quotes represent significant unfulfilled potential and might benefit from targeted follow-up campaigns or analysis to understand why they didn't convert. The high volume also suggests that a quote cleanup or archiving strategy might be beneficial for database management.

24. **Quotes with future policy termination dates:**
   ```sql
   SELECT COUNT(*) AS FutureTerminations
   FROM [Evolve].[dbo].[tblQuote]
   WHERE dtmPolicyTermination > GETDATE();
   ```
FutureTerminations
435

   **Insight:** Only 435 quotes have future policy termination dates. This small number suggests that either policy termination dates are typically not set in advance (possibly only being recorded when actual termination occurs), or that very few policies are scheduled for future termination. This could also indicate a high rate of ongoing policies without predetermined end dates, reflecting either strong customer retention or automatic renewal processes. Understanding why these specific policies have predetermined termination dates could reveal useful patterns.

---

