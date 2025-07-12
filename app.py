import streamlit as st
import pandas as pd
import datetime as dt

# Load stock price CSV
@st.cache_data
def load_stock_data():
    df = pd.read_csv("BFS_Share_Price.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
    df["Month-Year"] = df["Date"].dt.to_period("M")
    return df

stock_df = load_stock_data()

# Predefined answers from transcript analysis
transcript_answers = {
    "bagic motor": """
BAGIC is facing motor insurance headwinds due to no TP price hikes in 3 years, high combined ratios,
and selective underwriting in commercial vehicles. New vehicle sales were also weak in Q1 FY25.
""",
    "hero partnership": """
BAGIC tied up with Hero in Q1 FY25 to grow its 2-wheeler insurance, a segment it hadn’t tapped in 20 years.
""",
    "allianz exit": """
Allianz stake exit is under regulatory review since Q1 FY25. No material update yet, with IRDAI & CCI approval pending.
""",
    "bajaj markets": """
Bajaj Markets had 8.2M digital users in Q3 FY25, sourced 58k cards and disbursed ₹2000 Cr. On path to breakeven.
""",
    "cfo bagic": """
As CFO of BAGIC, I’d highlight strong underwriting results, cautious growth in motor, and robust solvency over 300%.
Despite regulatory impacts, we remain focused on balanced, long-term profitability.
"""
}

# Define function to answer stock queries
def handle_stock_query(query):
    query = query.lower()

    # Example: highest/average/lowest stock price in Mar-23
    for month in stock_df["Month-Year"].unique():
        mmyy = month.strftime("%b-%y").lower()
        if mmyy in query:
            filtered = stock_df[stock_df["Month-Year"] == month]
            max_price = filtered["Close Price"].max()
            min_price = filtered["Close Price"].min()
            avg_price = filtered["Close Price"].mean()
            return f"""📅 {mmyy.upper()}
- Highest: ₹{max_price:.2f}
- Lowest: ₹{min_price:.2f}
- Average: ₹{avg_price:.2f}"""

    # Compare from X to Y
    if "compare" in query and "to" in query:
        try:
            parts = query.split("compare")[1].split("to")
            start = pd.to_datetime("1-" + parts[0].strip(), format="%d-%b-%y").to_period("M")
            end = pd.to_datetime("1-" + parts[1].strip(), format="%d-%b-%y").to_period("M")
            selected = stock_df[(stock_df["Month-Year"] >= start) & (stock_df["Month-Year"] <= end)]
            summary = selected.groupby("Month-Year")["Close Price"].agg(["max", "min", "mean"]).round(2)
            return summary.to_string()
        except:
            return "❗ Couldn't parse date range. Try: Compare Jul-23 to Oct-23"

    return "❓ I couldn't find a stock query in your input."

# Define chatbot processor
def process_query(query):
    query = query.lower()

    # Match to transcript Q&A
    for key in transcript_answers:
        if key in query:
            return transcript_answers[key]

    # Match stock logic
    if any(word in query for word in ["price", "compare", "stock"]):
        return handle_stock_query(query)

    return "🤖 Sorry, I don't have an answer for that yet. Try another Bajaj-related question."

# -------- Streamlit UI -------- #
st.set_page_config(page_title="Bajaj Finserv AI Chatbot", page_icon="🤖")
st.title("🤖 Bajaj Finserv GenAI Chatbot")

query = st.text_input("Ask me anything about Bajaj Finserv 👇")

if query:
    response = process_query(query)
    st.markdown(response)
