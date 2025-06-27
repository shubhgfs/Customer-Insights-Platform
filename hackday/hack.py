import openai
import os
import re
from agno.tools import Toolkit
import json
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import pyodbc
import sqlalchemy
import urllib.parse

load_dotenv()

connstring="driver={ODBC Driver 17 for SQL Server};server=evm02.prod.db.hfs.local,1272;database=evolve;schema=dbo;Trusted_Connection=yes;"
evkpiconn = pyodbc.connect(connstring)
quoted_conn_str = urllib.parse.quote_plus(connstring)
engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted_conn_str))

class RecommendSIToolkit(Toolkit):
    def __init__(self, **kwargs):

        super().__init__(name='recommend_si_toolkit', **kwargs)        
        self.client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION_AQMAGENTICOS"),
        )
        self.deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS')

        self.register(self.recommend_premium)
        
        self.df_tblpremium = pd.read_csv(r'tblpremium.csv')
        self.df_tblProductBenefitRecommendedSI = pd.read_csv(r'tblProductBenefitRecommendedSI.csv')
        self.df_tblProductBenefitRecommendedSIBeta = pd.read_csv(r'tblProductBenefitRecommendedSIBeta.csv')

    def aggregate_suminsured_fixed_bands(tbl, band_width=5000):
        si_min = tbl['SumInsured'].min()
        si_max = tbl['SumInsured'].max()

        # Generate bins from si_min to si_max in increments of band_width
        bins = np.arange(si_min, si_max + band_width, band_width)

        # Assign SumInsured to bins, label bands as ranges like "min-max"
        labels = [f"{int(bins[i])}-{int(bins[i+1]-1)}" for i in range(len(bins)-1)]
        tbl['SumInsured_band'] = pd.cut(tbl['SumInsured'], bins=bins, labels=labels, include_lowest=True, right=False)

        # Aggregate TotalPremium stats per SumInsured band
        agg = tbl.groupby('SumInsured_band')['TotalPremium'].agg(['count', 'mean', 'min', 'max']).reset_index()

        # Find bands with zero count (no data)
        missing_bands = agg[agg['count'] == 0]['SumInsured_band'].tolist()

        # Impute missing bands by nearest non-empty band values (extrapolation)
        # Create a dictionary for fast lookup
        band_stats = agg.set_index('SumInsured_band')

        for band in missing_bands:
            idx = agg.index[agg['SumInsured_band'] == band][0]

            # Search previous bands
            prev_idx = idx - 1
            while prev_idx >= 0 and agg.loc[prev_idx, 'count'] == 0:
                prev_idx -= 1

            # Search next bands
            next_idx = idx + 1
            while next_idx < len(agg) and agg.loc[next_idx, 'count'] == 0:
                next_idx += 1

            prev_vals = None
            next_vals = None

            if prev_idx >= 0:
                prev_vals = agg.loc[prev_idx, ['mean', 'min', 'max']]

            if next_idx < len(agg):
                next_vals = agg.loc[next_idx, ['mean', 'min', 'max']]

            # Impute by averaging previous and next if both exist
            if prev_vals is not None and next_vals is not None:
                agg.loc[idx, ['mean', 'min', 'max']] = (prev_vals + next_vals) / 2
                agg.loc[idx, 'count'] = 0  # count stays zero, just stats filled
            elif prev_vals is not None:
                agg.loc[idx, ['mean', 'min', 'max']] = prev_vals
                agg.loc[idx, 'count'] = 0
            elif next_vals is not None:
                agg.loc[idx, ['mean', 'min', 'max']] = next_vals
                agg.loc[idx, 'count'] = 0
            else:
                # No neighbors found, leave as is or fill with NaNs
                agg.loc[idx, ['mean', 'min', 'max']] = np.nan

        return agg


    def generate_dynamic_sql_query(self, 
        product_code=None,
        benefit_code=None,
        gender_id=None,
        age=None,
        smoking_status_id=None,
        sum_insured=None,
        total_premium=None,
    ):
        base_query = """
            SELECT 
                q.Productcode,
                ab.benefitcode,
                ab.genderid,
                ab.age,
                ab.smokingstatusID,
                ab.SumInsured,
                q.TotalPremium
            FROM evolve.dbo.tblquote q
            INNER JOIN evolve.dbo.tblapplication a ON q.QuoteID = a.QuoteId
            INNER JOIN evolve.dbo.tblapplicationbenefit ab ON a.ApplicationId = ab.ApplicationId
            WHERE 1=1
            AND q.policystatusid in (30,40)
        """

        filters = []
        params = []

        if product_code:
            filters.append("q.Productcode = ?")
            params.append(product_code)
        if benefit_code:
            filters.append("ab.benefitcode = ?")
            params.append(benefit_code)
        if gender_id is not None:
            filters.append("ab.genderid = ?")
            params.append(gender_id)

        if age is not None:
            filters.append("ab.age = ?")
            params.append(age)

        if smoking_status_id is not None:
            filters.append("ab.smokingstatusID = ?")
            params.append(smoking_status_id)

        if sum_insured is not None:
            filters.append("ab.SumInsured = ?")
            params.append(sum_insured)

        if total_premium is not None:
            filters.append("q.TotalPremium = ?")
            params.append(total_premium)

        where_clause = " AND ".join(filters)
        final_query = base_query + (" AND " + where_clause if where_clause else "")

        return final_query, params

    def recommend_premium(self, input_data):
        print("Input Data:", input_data)

        # Extract filter values from input data
        product_code = input_data.get('product_code', None)
        benefit_code = input_data.get('benefit_code', None)
        gender = input_data.get('gender', None)
        smoker = input_data.get('smoker', None)
        age = input_data.get('age', None)
        premium = input_data.get('premium', None)
        sum_insured = input_data.get('sum_insured', None)
        
        query, params = self.generate_dynamic_sql_query(
            product_code=product_code,
            benefit_code=benefit_code,
            gender_id=gender,
            age=age,
            smoking_status_id=smoker,
            sum_insured=sum_insured,
            total_premium=premium,
        )

        upload = pd.read_sql(query, con=evkpiconn, params=params)

        tbl = upload[['SumInsured', 'TotalPremium']]

        bands = self.aggregate_suminsured_fixed_bands(tbl)

        print(bands)


        # # --- System prompt: Make the LLM act like a pricing assistant ---
        # system_prompt = """
        #     ###############################################################################
        #     # 1. ROLE & RULES
        #     ###############################################################################
        #     You are AURA, the Intelligent Insurance Pricing Assistant for Greenswan Financials.
        #     You must:
        #     • Accept **only** well-formed JSON as input.  
        #     • Return **only** well-formed JSON in your response—no extra text or comments.  
        #     • Always recommend a fair and optimized sum insured (SI) based on customer profile and premium budget.  
        #     • Justify recommendations with statistical insights from the provided dataset.  
        #     • If no matching records are available, return a polite error message in JSON.  
        #     • If customer premium is too low for any meaningful cover, suggest minimum viable SI if possible.

        #     ###############################################################################
        #     # 2. SYSTEM & ASSISTANT PERSONA
        #     ###############################################################################
        #     ## system
        #     You are a calm, professional insurance pricing advisor who always provides helpful, rational, and data-backed recommendations.
        #     You understand underwriting logic, pricing behavior, and customer affordability concerns.

        #     ## assistant (first reply payload)
        #     { "message": "Hi — I’m AURA, your intelligent insurance pricing assistant. How can I help you today?" }

        #     ###############################################################################
        #     # 3. FIXED RESPONSES / TEMPLATES
        #     ###############################################################################
        #     "CLARIFY":   { "error": "clarification_needed", "message": "Could you clarify your request?" }
        #     "NO_MATCH":  { "error": "no_data_found", "message": "No similar profiles found within the budget range." }
        #     "GOODBYE":   { "message": "Thank you for using Greenswan Pricing Assistant. Have a great day!" }

        #     ###############################################################################
        #     # 4. FUNCTION_CALLS  (OPTIONAL)
        #     ###############################################################################
        #     None for now – all reasoning is local to the assistant. Future APIs may include:
        #     recommend_si_from_budget(product_code, benefit_code, age, gender, smoker, cover_type, budget)

        #     ###############################################################################
        #     # 5. ERROR / EDGE-CASE HANDLING  (OPTIONAL)
        #     ###############################################################################
        #     If input JSON is malformed → return  
        #     { "error": "invalid_json", "message": "Input must be valid JSON." }

        #     If premium is below minimum viable threshold (e.g., < $100) →  
        #     { "warning": "low_premium", "message": "The premium is very low; expected sum insured will be limited." }

        #     ###############################################################################
        #     # 6. DOMAIN KNOWLEDGE  (OPTIONAL)
        #     ###############################################################################
        #     • ProductCode and BenefitCode map to specific life insurance offerings.  
        #     • Gender: 0 = Female, 1 = Male  
        #     • Smoker: 0 = No, 1 = Yes  
        #     • CoverType is an integer that defines type of benefit rider  
        #     • Premium is in AUD  
        #     • Sum Insured is historically mapped by customer profile and age bracket  
        #     • All recommendations should be derived from filtered premium and SI statistics only  
        #     • Use mean, min, and max values for reasoning, not outliers  

        #     ###############################################################################
        #     # 7. SAMPLE USER INPUT FORMAT
        #     ###############################################################################
        #     {
        #     "product_code": "AFP",
        #     "benefit_code": "DTH",
        #     "gender": 0,
        #     "smoker": 0,
        #     "age": 17,
        #     "cover_type": 1,
        #     "max_affordable_premium": 3000.0,
        #     "premium_summary": {
        #         "Premium": {
        #         "count": 8,
        #         "mean": 2467.5,
        #         "std": 371.4,
        #         "min": 1875.0,
        #         "25%": 2250.0,
        #         "50%": 2500.0,
        #         "75%": 2750.0,
        #         "max": 2975.0
        #         }
        #     },
        #     "sum_insured_summary": {
        #         "RecommendedSI": {
        #         "count": 8,
        #         "mean": 150000.0,
        #         "std": 12000.0,
        #         "min": 130000.0,
        #         "25%": 140000.0,
        #         "50%": 150000.0,
        #         "75%": 160000.0,
        #         "max": 170000.0
        #         }
        #     }
        #     }

        #     ###############################################################################
        #     # 8. EXPECTED ASSISTANT RESPONSE FORMAT
        #     ###############################################################################
        #     {
        #     "recommended_sum_insured": 145000,
        #     "justification": "Based on the customer's profile and a maximum affordable premium of $3000, similar customers typically receive between $130,000 and $170,000 in coverage. The average sum insured is $150,000. To stay within budget, a recommended sum insured of $145,000 balances affordability with appropriate coverage."
        #     }

        # """

        # # --- User query: Provide the customer info and the statistical summary ---
        # query = (
        #     f"A customer has approached us for an insurance product. Based on their full profile and chosen benefit, "
        #     f"they received a premium quote, but they cannot afford to pay that much.\n\n"
        #     f"Their profile is:\n"
        #     f"- Age: {age}\n"
        #     f"- Gender: {gender}\n"
        #     f"- Smoker: {smoker}\n"
        #     f"- Product Code: {product_code}\n"
        #     f"- Benefit Code: {benefit_code}\n"
        #     f"- Cover Type: {cover_type}\n\n"
        #     f"They were originally quoted a higher premium but have now indicated they can only afford: ${premium:,.2f}\n\n"
        #     f"We have filtered historical data to find similar customers (within ±3 years of age) with the same product, benefit, "
        #     f"gender, smoker status, and cover type. The premiums of these matching records are all less than or equal to ${premium:,.2f}.\n\n"
        #     f"Here is the Statistical Summary of Premiums from matching profiles:\n{json.dumps(description_premium, indent=2)}\n\n"
        #     f"And here is the Statistical Summary of Recommended Sum Insured (SI) for customers with the same product and benefit at the closest age bracket:\n"
        #     f"{json.dumps(description_SI, indent=2)}\n\n"
        #     f"Can you:\n"
        #     f"- Recommend a fair and optimized Sum Insured this customer should be offered given their budget?\n"
        #     f"- Briefly explain why, using statistics from the dataset?\n\n"
        #     f"This will help us retain the customer by tailoring the coverage to what they can afford, instead of losing the sale."
        # )

        # # LLM call with system context
        # messages = [
        #     {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
        #     {"role": "user", "content": [{"type": "text", "text": query}]}
        # ]


        # response = self.client.chat.completions.create(
        #     model=self.deployment,
        #     messages=messages,
        #     temperature=0
        # )

        # response_text = response.choices[0].message.content.strip()
        # return response_text

# a = RecommendSIToolkit()
# input_data = {
#     "product_code": "AFP",         # string matches dtype: object
#     "benefit_code": "DTH",         # string matches dtype: object
#     "gender": 0,                   # integer matches dtype: int64
#     "smoker": 0,                   # integer matches dtype: int64
#     "age": 52,                     # integer matches dtype: int64
#     "premium": 3000.0,             # float matches dtype: float64
#     "cover_type": 1                # integer matches dtype: int64
# }
# result = a.recommend_premium(input_data)
# print("Result:", result)