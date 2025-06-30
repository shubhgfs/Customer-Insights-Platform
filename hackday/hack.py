import openai
import os
import re
from agno.tools import Toolkit
import json
from dotenv import load_dotenv
import numpy as np
import pandas as pd

load_dotenv()

print(os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"))
print(os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"))
print(os.getenv("AZURE_OPENAI_API_VERSION_AQMAGENTICOS"))
print(os.getenv('AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS'))

class RecommendSIToolkit(Toolkit):
    def __init__(self, **kwargs):

        super().__init__(name='recommend_si_toolkit', **kwargs)        
        self.client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION_AQMAGENTICOS")
        )
        self.deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS')

        self.register(self.recommend_premium)
        
        self.df_tblpremium = pd.read_csv(r'tblpremium.csv')
        self.df_tblProductBenefitRecommendedSI = pd.read_csv(r'tblProductBenefitRecommendedSI.csv')
        self.df_tblProductBenefitRecommendedSIBeta = pd.read_csv(r'tblProductBenefitRecommendedSIBeta.csv')
        self.df_tblQAI = pd.read_excel(r'tblQAI.xlsx')

    def aggregate_suminsured_fixed_bands(self, tbl, band_width=5000):
        si_min = tbl['sum_insured'].min()
        si_max = tbl['sum_insured'].max()

        # Generate bins from si_min to si_max in increments of band_width
        bins = np.arange(si_min, si_max + band_width, band_width)

        # Label bands like "10000-14999"
        labels = [f"{int(bins[i])}-{int(bins[i+1]-1)}" for i in range(len(bins)-1)]
        tbl['sum_insured_band'] = pd.cut(tbl['sum_insured'], bins=bins, labels=labels, include_lowest=True, right=False)

        # Aggregate both sum_insured and premium stats
        agg = tbl.groupby('sum_insured_band').agg(
            count=('premium', 'count'),
            premium_mean=('premium', 'mean'),
            premium_min=('premium', 'min'),
            premium_max=('premium', 'max'),
            sum_insured_mean=('sum_insured', 'mean'),
            sum_insured_min=('sum_insured', 'min'),
            sum_insured_max=('sum_insured', 'max')
        ).reset_index()

        # Handle empty bands (where count == 0)
        missing_bands = agg[agg['count'] == 0]['sum_insured_band'].tolist()
        for band in missing_bands:
            idx = agg.index[agg['sum_insured_band'] == band][0]

            # Look for previous non-empty band
            prev_idx = idx - 1
            while prev_idx >= 0 and agg.loc[prev_idx, 'count'] == 0:
                prev_idx -= 1

            # Look for next non-empty band
            next_idx = idx + 1
            while next_idx < len(agg) and agg.loc[next_idx, 'count'] == 0:
                next_idx += 1

            prev_vals = agg.loc[prev_idx] if prev_idx >= 0 else None
            next_vals = agg.loc[next_idx] if next_idx < len(agg) else None

            # Impute with average of neighbors if both exist
            if prev_vals is not None and next_vals is not None:
                for col in ['premium_mean', 'premium_min', 'premium_max',
                            'sum_insured_mean', 'sum_insured_min', 'sum_insured_max']:
                    agg.at[idx, col] = (prev_vals[col] + next_vals[col]) / 2
            elif prev_vals is not None:
                for col in ['premium_mean', 'premium_min', 'premium_max',
                            'sum_insured_mean', 'sum_insured_min', 'sum_insured_max']:
                    agg.at[idx, col] = prev_vals[col]
            elif next_vals is not None:
                for col in ['premium_mean', 'premium_min', 'premium_max',
                            'sum_insured_mean', 'sum_insured_min', 'sum_insured_max']:
                    agg.at[idx, col] = next_vals[col]
            else:
                # If no neighbors, fill with NaN
                for col in ['premium_mean', 'premium_min', 'premium_max',
                            'sum_insured_mean', 'sum_insured_min', 'sum_insured_max']:
                    agg.at[idx, col] = np.nan

        return agg


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
        idn = input_data.get('idn', None)

        upload = self.df_tblQAI

        # Apply filters for all params if present
        tbl = upload.copy()
        print(tbl.head())
        if product_code is not None:
            tbl = tbl[tbl['product_code'] == product_code]
        if benefit_code is not None:
            tbl = tbl[tbl['benefit_code'] == benefit_code]
        if gender is not None:
            tbl = tbl[tbl['gender'] == gender]
        if smoker is not None:
            tbl = tbl[tbl['smoker'] == smoker]
        if age is not None:
            tbl = tbl[tbl['age'] == age]
        if premium is not None:
            tbl = tbl[tbl['premium'] <= premium]
        if sum_insured is not None:
            tbl = tbl[tbl['sum_insured'] == sum_insured]

        tbl = tbl[['sum_insured', 'premium']]

        bands = self.aggregate_suminsured_fixed_bands(tbl)
        bands = bands[['premium_mean', 'premium_min', 'premium_max', 'sum_insured_mean', 'sum_insured_min', 'sum_insured_max']]
        records_dict = bands.to_dict(orient='records')

        print(bands)


        # --- System prompt: Make the LLM act like a pricing assistant ---
        system_prompt = """
            ###############################################################################
            # 1. ROLE & RULES
            ###############################################################################
            You are AURA, the Intelligent Insurance Pricing Assistant for Greenswan Financials.
            You must:
            • Accept **only** well-formed JSON as input.  
            • Return **only** well-formed JSON in your response—no extra text or comments.  
            • Always recommend a fair and optimized sum insured (SI) based on customer profile and premium budget.  
            • Justify recommendations with statistical insights from the provided dataset.  
            • If no matching records are available, return a polite error message in JSON.  
            • If customer premium is too low for any meaningful cover, suggest minimum viable SI if possible.

            ###############################################################################
            # 2. SYSTEM & ASSISTANT PERSONA
            ###############################################################################
            ## system
            You are a calm, professional insurance pricing advisor who always provides helpful, rational, and data-backed recommendations.
            You understand underwriting logic, pricing behavior, and customer affordability concerns.

            ## assistant (first reply payload)
            { "message": "Hi — I’m AURA, your intelligent insurance pricing assistant. How can I help you today?" }

            ###############################################################################
            # 3. FIXED RESPONSES / TEMPLATES
            ###############################################################################
            "CLARIFY":   { "error": "clarification_needed", "message": "Could you clarify your request?" }
            "NO_MATCH":  { "error": "no_data_found", "message": "No similar profiles found within the budget range." }
            "GOODBYE":   { "message": "Thank you for using Greenswan Pricing Assistant. Have a great day!" }

            ###############################################################################
            # 4. FUNCTION_CALLS  (OPTIONAL)
            ###############################################################################
            None for now – all reasoning is local to the assistant. Future APIs may include:
            recommend_si_from_budget(product_code, benefit_code, age, gender, smoker, cover_type, budget)

            ###############################################################################
            # 5. ERROR / EDGE-CASE HANDLING  (OPTIONAL)
            ###############################################################################
            If input JSON is malformed → return  
            { "error": "invalid_json", "message": "Input must be valid JSON." }

            If premium is below minimum viable threshold (e.g., < $100) →  
            { "warning": "low_premium", "message": "The premium is very low; expected sum insured will be limited." }

            ###############################################################################
            # 6. DOMAIN KNOWLEDGE  (OPTIONAL)
            ###############################################################################
            • ProductCode and BenefitCode map to specific life insurance offerings.  
            • Gender: 0 = Female, 1 = Male  
            • Smoker: 0 = No, 1 = Yes  
            • CoverType is an integer that defines type of benefit rider  
            • Premium is in AUD  
            • Sum Insured is historically mapped by customer profile and age bracket  
            • All recommendations should be derived from filtered premium and SI statistics only  
            • Use mean, min, and max values for reasoning, not outliers  

            ###############################################################################
            # 9. OUTPUT RULES (STRICT FORMAT)
            ###############################################################################
            You MUST return only a valid JSON object with the following structure:
            {
            "data": [...]
            }

            Where [...] is a JSON array of records derived from the dataset. Do not include:
            - Explanations
            - Extra text
            - Comments
            - Markdown
            - Greetings
            - Warnings

            Only return the final JSON object. If you cannot generate a valid response, return:
            { "error": "no_data_found", "message": "No similar profiles found." }

        """

        system_prompt = system_prompt.replace('<records_dict>', json.dumps(records_dict, indent=2))

        query = (
            f"A customer has approached us for an insurance product. Based on their full profile and chosen benefit, "
            f"they received a premium quote, but they cannot afford to pay that much.\n\n"
            f"Their profile is:\n"
            f"- Age: {age}\n"
            f"- Gender: {gender}\n"
            f"- Smoker: {smoker}\n"
            f"- Product Code: {product_code}\n"
            f"- Benefit Code: {benefit_code}\n"
            f"We have filtered historical data to find similar customers (within ±3 years of age) with the same product, benefit, "
            f"Here is the Statistical Summary of Premiums from matching profiles:\n{json.dumps(records_dict, indent=2)}\n\n"
            f"And here is the Statistical Summary of Recommended Sum Insured (SI) for customers with the same product and benefit at the closest age bracket:\n"
            f"{json.dumps(records_dict, indent=2)}\n\n"
            f"Can you:\n"
            f"- Recommend a fair and optimized Sum Insured this customer should be offered given their budget?\n"
            f"- Briefly explain why, using statistics from the dataset?\n\n"
            f"This will help us retain the customer by tailoring the coverage to what they can afford, instead of losing the sale."
        )

        # LLM call with system context
        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": query}]}
        ]


        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=0
        )

        response_text = response.choices[0].message.content.strip()

        data = {
            "response_text": response_text,
            "records_dict": records_dict
        }

        with open(f'response_{idn}.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()

        # Validate JSON response
        return 'All Successful'
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