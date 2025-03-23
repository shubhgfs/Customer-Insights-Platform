import streamlit as st

def get_product_name():
    return st.query_params.get("product_name")

product_name = get_product_name()

st.title("💡 How to Use the Customer Insights Chatbot & Agents")

st.markdown(f"""
# Overview
In this guide, you’ll learn how to leverage the Customer Insights Chatbot and AI-powered agents to enhance your efforts for {product_name}. These tools will help you gain insights, improve your messaging, and optimize your content.
""")
