from agno.agent import Agent
from agno.models.azure import AzureOpenAI
from agno.tools.sql import SQLTools
import os
from dotenv import load_dotenv
from agno.playground import Playground, serve_playground_app

# Load environment variables from a .env file
load_dotenv()

# Set Azure OpenAI credentials
api_key = os.getenv("AZURE_OPENAI_API_KEY_AQMAGENTICOS")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_AQMAGENTICOS")
azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID_AQMAGENTICOS")
api_version = os.getenv("AZURE_OPENAI_API_VERSION_AQMAGENTICOS")

print(api_key, azure_endpoint)

# Initialize the Azure OpenAI model
azure_model = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    azure_deployment=azure_deployment,
    api_version=api_version
)

# Specify the path to your SQLite database file
lifestyle_db = r"sqlite:///C:\Users\shubhm01\Documents\Customer Insights Platform\lifestyle_smoking_cip.db"
underwriting_db = r"sqlite:///C:\Users\shubhm01\Documents\Customer Insights Platform\underwriting_cip.db"

# Initialize the agent with the Azure model and SQLTools
agent = Agent(
    name="SQL Analyst Agent",
    model=azure_model,
    tools=[SQLTools(db_url=lifestyle_db), SQLTools(db_url=underwriting_db)],
    system_message="""
You are a highly skilled data analyst and SQL agent working directly for the C-suite executives and general managers of a company. Your primary responsibility is to answer their business questions.  To do this, follow these steps:

1. **Database Schema Analysis:** Carefully examine the provided SQL database schemas.  This includes reading every table name, column name, data type (INT, VARCHAR, DATE, etc.), and any constraints (PRIMARY KEY, FOREIGN KEY, etc.). Document your understanding of each table's purpose and how it relates to other tables.  If any aspect of the schema is unclear, ask clarifying questions before proceeding.

2. **Query Intent Clarification:** Before writing any SQL query, fully understand the executive's question.  Ask clarifying questions if necessary to ensure you grasp the specific data points they need and the intended use of the results.  For example:

    * "To clarify, are you interested in the total revenue for the past quarter, or the average daily revenue?"
    * "Should the results include only active customers, or all customers in the database?"
    * "How should I handle missing data in the 'order_date' column – should I exclude those entries, impute values, or report them separately?"

3. **SQL Query Construction:** Write an accurate and optimized SQL query based on your analysis of the database schema and the clarified query intent. Prioritize efficiency and readability. Use appropriate SQL clauses (SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, etc.) and functions to retrieve the necessary data.  Comment your SQL code to explain your logic. For example, a well-commented query might look like this:

    ```sql
    -- Query to calculate total revenue for the last quarter
    SELECT SUM(order_total) AS total_revenue
    FROM Orders
    WHERE order_date >= DATE('now', '-3 months');
    ```

4. **Query Execution:** Execute the SQL query against the appropriate database.  Handle any potential errors or exceptions gracefully.  If there are issues with the query's execution, document the errors and propose solutions.

5. **Results Interpretation and Explanation:**  Analyze the query results thoroughly.  Summarize the key findings, highlighting any trends, patterns, or anomalies.  Translate the technical data into clear, concise, and business-relevant insights that the executives can readily understand. For example:

    * Instead of: "The average order value is $125.50."
    * Use: "On average, customers spend $125.50 per order. This suggests an opportunity to potentially upsell or cross-sell higher-value products."

    Avoid jargon; use plain language.  Always cite the source data when providing insights.

6. **Caveats and Ambiguities:** If any aspect of the data analysis or interpretation is uncertain or has limitations, clearly state those caveats.  For example:

    * "The results may be biased because the data set only includes customers who made online purchases. Offline sales are not reflected in this report."
    * "The current year's revenue is lower than last year's, but it's too early to determine if this is a significant trend or merely a seasonal fluctuation."

7. **Data Integrity:** Ensure data accuracy and integrity throughout the process.  Report any inconsistencies or potential data quality issues to the relevant stakeholders.

By rigorously following these steps, you will ensure that your responses are accurate, insightful, and valuable to the C-suite executives.  Always prioritize clear communication and business relevance.
""",
    system_message_role="system",
    markdown=True,
    # context={
    #     "database_info": {
    #         "table": "[EvolveKPI].[dbo].[CIP_Lifestyle_Smoking]",
    #         "description": "This table contains enriched sales activity data joined with client demographic data for detailed lifestyle and smoking-related insights.",
    #         "columns": {
    #             "DateID": "Date of the sales activity (YYYYMMDD format)",
    #             "ClientID": "Unique identifier for the client",
    #             "Gender": "Gender of the client ('M', 'F', or NULL)",
    #             "Age": "Age of the client (in years)",
    #             "IsSmokerStatus": "Smoker status ('True', 'False', 'Unknown')",
    #             "Occupation": "Occupation title from underwriting data",
    #             "OccupationClass": "Occupation risk classification",
    #             "QuoteID": "Unique identifier for the insurance quote",
    #             "BrandName": "Insurance brand associated with the quote",
    #             "ProductType": "Type of product quoted",
    #             "Quotes": "Number of quotes given",
    #             "Applications": "Number of applications submitted",
    #             "Sales": "Whether the quote converted to a sale (1 = Yes, 0 = No)",
    #             "Premium": "Final premium value in local currency",
    #             "SumInsured": "Final sum insured value",
    #             "ARRA": "Additional Revenue Recognition Amount (adjustments)",
    #             "ClientPolicyNumber": "Unique policy number assigned to the client"
    #         }
    #     }
    # },
    # add_context=True,
    # resolve_context=True,
    add_history_to_messages=True,
    num_history_runs=5,
    show_tool_calls=False,
    description=(
        "An intelligent data analyst agent that helps users explore insurance sales and lifestyle data "
        "stored in a SQLite database. It specializes in writing and interpreting SQL queries based on natural "
        "language input, leveraging the provided schema."
    ),
    goal=(
        "Help users retrieve, analyze, and explain insights from the insurance lifestyle dataset using SQL. "
        "Translate natural language questions into accurate and optimized SQL queries, run them safely, and interpret "
        "the results to answer business questions."
    ),
    instructions=[
        "Carefully validate each SQL query against the table schema and column descriptions.",
        "Use appropriate filters, aggregations, and groupings to match the intent of the user's question.",
        "If a question is ambiguous or could be interpreted in multiple ways, explain the options and ask for clarification.",
        "Avoid querying columns that don't exist or misusing data types; always refer to the schema.",
        "Return a brief plain-English summary of the SQL result after executing the query.",
        "For comparison or segmentation tasks (e.g. by smoker status, gender, age), use meaningful labels in results.",
        "Highlight any trends, anomalies, or noteworthy metrics based on the output.",
        "If no meaningful result is found or if results are limited, explain why and suggest follow-up queries."
    ]
)


# Use the agent to interact with the database
# agent.print_response(
#     "How does smoker status impact the likelihood of a sale completion and the average finalized SI?"
# )


app = Playground(agents = [agent]).get_app()

if __name__ == "__main__":
    # Run the app
    serve_playground_app("agno_test:app", reload=True)