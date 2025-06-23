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
            api_key=os.getenv("AZURE_API_KEY_AQMAGENTICOS"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT_AQMAGENTICOS"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION_AQMAGENTICOS"),
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS")
        
        self.df_tblpremium = pd.read_csv(r'hackday\tblpremium.csv')
        self.df_tblProductBenefitRecommendedSI = pd.read_csv(r'hackday\tblProductBenefitRecommendedSI.csv')
        self.df_tblProductBenefitRecommendedSIBeta = pd.read_csv(r'hackday\tblProductBenefitRecommendedSIBeta.csv')
        
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

        # Generate statistical description of matching records
        description = sub.describe().to_dict()
        premium_stats = description.get("Premium", {})

        # --- System prompt: Make the LLM act like a pricing assistant ---
        system_prompt = (
            "You are an experienced insurance pricing assistant. "
            "Based on the provided statistical summary of premiums from similar customer profiles, "
            "please analyze the data and provide a concise explanation of the expected premium. "
            "Highlight important statistics such as the mean, minimum, and maximum values. "
            "Provide recommendations on what premium the customer might pay, along with your rationale."
        )

        # --- User query: Provide the customer info and the statistical summary ---
        query = (
            "Customer Profile Summary:\n"
            f"- Age: {age}\n"
            f"- Gender (0 for female, 1 for male): {gender}\n"
            f"- Smoker Status (0 for non-smoker, 1 for smoker): {smoker}\n"
            f"- Product Code: {product_code}\n"
            f"- Benefit Code: {benefit_code}\n\n"
            "Statistical Summary of Premiums:\n"
            f"{json.dumps(premium_stats, indent=2)}\n\n"
            "Based on these details, please provide a recommended premium and a brief explanation."
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

        return response
    
a = RecommendSIToolkit()
input_data = {
    "product_code": "AFP",         # string matches dtype: object
    "benefit_code": "DTH",         # string matches dtype: object
    "gender": 0,                   # integer matches dtype: int64
    "smoker": 0,                   # integer matches dtype: int64
    "age": 17,                     # integer matches dtype: int64
    "premium": 3000.0,             # float matches dtype: float64
    "cover_type": 1                # integer matches dtype: int64
}
result = a.recommend_premium(input_data)
print("Result:", result)