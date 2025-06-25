import openai
import os
from agno.tools import Toolkit
import json
from dotenv import load_dotenv
import numpy as np
import pandas as pd

load_dotenv()

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

    def recommend_premium(self, input_data):
        """ 
        Recommend premium based on input data criteria.
        
        Args:
            input_data (dict): Dictionary containing filter criteria:
                - product_code: Product code (str)
                - benefit_code: Benefit code (str)
                - gender: Gender code (int, 0 for female, 1 for male)
                - smoker: Smoker status (int, 0 for non-smoker, 1 for smoker)
                - age: Age (int)
                - premium: Maximum premium amount (float)
                - cover_type: Cover type code (int)
        
        Returns:
            dict: Statistical description of matching records
        """
        # For debugging purposes, you can uncomment these lines
        # print("Input Data:", input_data)
        # print("Sample rows from DataFrame:")
        # sample_df = self.df_tblpremium[['ProductCode', 'Age', 'BenefitCode', 'CoverType', 'Gender', 'Smoker', 'Premium']].head(5)
        # print(sample_df)
        
        # Extract relevant columns
        df = self.df_tblpremium[['ProductCode', 'Age', 'BenefitCode', 'CoverType', 'Gender', 'Smoker', 'Premium']]

        # Extract filter values from input data
        product_code = input_data.get('product_code')
        benefit_code = input_data.get('benefit_code')
        gender = input_data.get('gender')
        smoker = input_data.get('smoker')
        age = input_data.get('age')
        premium = input_data.get('premium')
        cover_type = input_data.get('cover_type')
        
        # Apply filters to get matching records
        sub = df[
            (df['ProductCode'] == product_code) &
            (df['BenefitCode'] == benefit_code) &
            (df['Gender'] == gender) &
            (df['Smoker'] == smoker) &
            (df['Age'] >= age - 3) &
            (df['Age'] <= age + 3) &
            (df['Premium'] <= premium) &
            (df['CoverType'] == cover_type)
        ]

        # Check if any matches were found
        if sub.shape[0] == 0:
            return {"message": "No matching records found. Please check your filter criteria."}
        else:
            selected_age = sub.loc[sub['Premium'].idxmax(), 'Age']

        si = self.df_tblProductBenefitRecommendedSI[
            (self.df_tblProductBenefitRecommendedSI['ProductCode'] == product_code) &
            (self.df_tblProductBenefitRecommendedSI['BenefitCode'] == benefit_code) &
            (self.df_tblProductBenefitRecommendedSI['Age'] == selected_age)
        ]

        si = si[['ProductCode', 'BenefitCode', 'Age', 'RecommendedSI']]

        description_premium = sub.describe(). to_dict()
        description_SI = si.describe().to_dict()

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
            # 7. SAMPLE USER INPUT FORMAT
            ###############################################################################
            {
            "product_code": "AFP",
            "benefit_code": "DTH",
            "gender": 0,
            "smoker": 0,
            "age": 17,
            "cover_type": 1,
            "max_affordable_premium": 3000.0,
            "premium_summary": {
                "Premium": {
                "count": 8,
                "mean": 2467.5,
                "std": 371.4,
                "min": 1875.0,
                "25%": 2250.0,
                "50%": 2500.0,
                "75%": 2750.0,
                "max": 2975.0
                }
            },
            "sum_insured_summary": {
                "RecommendedSI": {
                "count": 8,
                "mean": 150000.0,
                "std": 12000.0,
                "min": 130000.0,
                "25%": 140000.0,
                "50%": 150000.0,
                "75%": 160000.0,
                "max": 170000.0
                }
            }
            }

            ###############################################################################
            # 8. EXPECTED ASSISTANT RESPONSE FORMAT
            ###############################################################################
            {
            "recommended_sum_insured": 145000,
            "justification": "Based on the customer's profile and a maximum affordable premium of $3000, similar customers typically receive between $130,000 and $170,000 in coverage. The average sum insured is $150,000. To stay within budget, a recommended sum insured of $145,000 balances affordability with appropriate coverage."
            }

        """

        # --- User query: Provide the customer info and the statistical summary ---
        query = (
            f"A customer has approached us for an insurance product. Based on their full profile and chosen benefit, "
            f"they received a premium quote, but they cannot afford to pay that much.\n\n"
            f"Their profile is:\n"
            f"- Age: {age}\n"
            f"- Gender: {gender}\n"
            f"- Smoker: {smoker}\n"
            f"- Product Code: {product_code}\n"
            f"- Benefit Code: {benefit_code}\n"
            f"- Cover Type: {cover_type}\n\n"
            f"They were originally quoted a higher premium but have now indicated they can only afford: ${premium:,.2f}\n\n"
            f"We have filtered historical data to find similar customers (within ±3 years of age) with the same product, benefit, "
            f"gender, smoker status, and cover type. The premiums of these matching records are all less than or equal to ${premium:,.2f}.\n\n"
            f"Here is the Statistical Summary of Premiums from matching profiles:\n{json.dumps(description_premium, indent=2)}\n\n"
            f"And here is the Statistical Summary of Recommended Sum Insured (SI) for customers with the same product and benefit at the closest age bracket:\n"
            f"{json.dumps(description_SI, indent=2)}\n\n"
            f"Can you:\n"
            f"- Recommend a fair and optimized Sum Insured this customer should be offered given their budget?\n"
            f"- Briefly explain why, using statistics from the dataset?\n\n"
            f"This will help us retain the customer by tailoring the coverage to what they can afford, instead of losing the sale."
        )

        # LLM call with system context
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {query}"}
        ]

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages
        )

        return response.choices[0].message.content
    
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