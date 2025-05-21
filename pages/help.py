import streamlit as st

def get_product_name():
    return st.query_params.get("product_name")

product_name = get_product_name()

st.title("💡 How to Use the Marketing Chatbot & Agents")

st.markdown(f"""
# Overview
In this guide, you’ll learn how to leverage the Marketing Chatbot and AI-powered agents to enhance your marketing efforts for {product_name}. These tools will help you gain insights, improve your messaging, and optimize your content.
""")

st.markdown("---")

st.markdown("## ➡️ How to Use the Marketing Chatbot")
st.markdown("""
The chatbot helps you analyze customer interactions, understand feedback, identify pain points, and improve your marketing strategies.
""")
with st.expander("Click to Expand for Details!"):
    st.markdown(f"""
        ### How can you use this chatbot?
        - ✅ **Understand Customer Feedback** – Learn why customers do or don’t buy {product_name}.
        - ✅ **Identify Sales Trends** – Discover patterns in customer objections and successful sales conversations.
        - ✅ **Discover Pain Points** – Pinpoint common concerns or barriers preventing conversions for {product_name}.
        - ✅ **Analyze Sentiments** – Explore how customers feel about pricing, features, or sales pitches for {product_name}.
        - ✅ **Compare Product Performance** – Find out how {product_name} is perceived compared to others.

        ### Example Questions:
        - 💬 "What objections do customers have about {product_name}?"
        - 💬 "Why do customers say no to {product_name}?"
        - 💬 "What are the top concerns about {product_name}?"
        - 💬 "What positive feedback do customers give about {product_name}?"
        - 💬 "How do customers react to {product_name}'s pricing?"
        - 💬 "Are there any emerging trends in customer feedback about {product_name}?"
    """)

st.markdown("---")

st.markdown("## ➡️ How to Use the Marketing Agents")
st.markdown("""
These AI-powered agents are designed to help you generate optimized marketing content across different platforms, based on real customer data.
""")
with st.expander("Click to Expand for Details!"):
    st.markdown("""
    - **📢 Facebook Ad Copy Agent** – Crafts high-converting Facebook ad copy using customer insights from sales calls.
    - **🔎 Google Keyword (AdWords) Agent** – Generates targeted Google AdWords keywords based on customer language and behavior.
    - **🎶 Radio Jingle Agent** – Creates catchy radio jingles using feedback and product insights.
    - **🎬 Video Script Agent** – Writes compelling video scripts grounded in real sales interactions to boost customer engagement.

    Combine these agents to create cohesive and impactful marketing assets!
    """)

st.markdown("---")

st.markdown("## ➡️ How to Use Both the Chatbot & Agents Together")
st.markdown("""
Leverage both the chatbot and agents simultaneously for a more comprehensive marketing strategy, combining customer insights with tailored content creation.
""")

with st.expander("Example 1: Customer Satisfaction Insights to Ad Campaigns"):
    st.markdown(f"""
        **(📢 Facebook Agent)** "Give me the top 10 keywords based on customer interactions from the call recordings that show why customers are happy with {product_name}."
        *(Model fetches relevant customer satisfaction feedback and generates a list of targeted keywords.)*

        **(🎬 Video Script Agent)** "Generate a video script based on the keywords provided earlier to drive more sales for {product_name}."
        *(Model creates a lively, engaging video ad script using the identified keywords.)*

        **(🎶 Radio Jingle Agent)** "Generate a catchy jingle based on the preferences of existing happy customers."
        *(Model creates a jingle based on customer feedback.)*
    """)

with st.expander("Example 2: Addressing Customer Objections with Multi-Channel Marketing"):
    st.markdown(f"""
        **(🔎 Google Keyword Agent)** "Find common objections customers have about {product_name} based on past interactions."
        *(Model extracts top objections and customer concerns from sales conversations.)*

        **(📢 Facebook Agent)** "Create an ad copy that directly addresses these concerns and reassures potential customers."
        *(Model generates persuasive ad copy tailored to overcoming objections.)*

        **(🎬 Video Script Agent)** "Write a 30-second video script to tackle these concerns with strong selling points."
        *(Model generates a short video ad script focused on addressing objections.)*
    """)

with st.expander("Example 3: Launching a New Product with Multi-Platform Content"):
    st.markdown(f"""
        **(📢 Facebook Agent)** "Generate an engaging Facebook ad introducing {product_name} to a new audience using insights from customer interactions."
        *(Model creates an ad highlighting the product’s unique selling points.)*

        **(🔎 Google Keyword Agent)** "Suggest high-converting Google keywords based on customer language and interactions."
        *(Model generates top-performing search keywords.)*

        **(🎶 Radio Jingle Agent)** "Write a catchy jingle that makes {product_name} memorable on the radio."
        *(Model creates a rhythmic, catchy jingle.)*
    """)

st.markdown("---")

st.markdown("### Start Using the Chatbot & Agents")
st.markdown(f"""
Leverage customer insights and AI-powered agents to optimize your marketing for {product_name}. Enter the product name and start generating targeted content today!
""")
