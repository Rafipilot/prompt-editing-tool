import streamlit as st
from dotenv import load_dotenv
import os
from pymongo import MongoClient, DESCENDING

load_dotenv()

mongo_uri = os.environ["MONGODB_URI"]
client = MongoClient(mongo_uri)

db = client["companies"]
reports_collection = db["company_research_reports"]


match_step_name_to_path = {
    "company-research": "company-research.md",
    "qualitative-analysis": "qualitative-analysis.md",
    "industry-and-strategy-context": "industry-and-strategy-context.md",
    "core-drivers": "core-drivers-summary.md",
    "attractiveness-of-end-market": "attractiveness-of-end-market.md",
    "competition": "competition.md",
    "m&a-and-being-acquired": "m&a-and-being-acquired.md",
    "business-model": "business-model.md",
    "defensibility-and-moats": "defensibility-and-moats.md",
    "gross-margin-drivers": "gross-margin-drivers.md",
    "operating-expenses-drivers": "operating-expenses-drivers.md",
    "leverage-and-cost-of-capital-drivers": "leverage-and-cost-of-capital-drivers.md",
    "roic-drivers": "roic-drivers.md",
    "management-team": "management-team.md",
    "addressable-market-and-growth": "addressable-market-and-growth.md",
    "revenue-drivers": "revenue-drivers.md",
    "long-term-growth": "long-term-growth.md",
    "net-income-drivers": "net-income-drivers.md",
    "product-value-add-and-pricing-power": "product-value-add-and-pricing-power.md",
    "cyclicality": "cyclicality.md",
    "balance-sheet-drivers": "balance-sheet-drivers.md",
    "customer-profile-and-customer-concentration": "customer-profile-and-customer-concentration.md",
    "operating-leverage-and-unit-economics-drivers": "operating-leverage-and-unit-economics-drivers.md",
    "product-highlights": "product-highlights.md",
    "ownership-and-technicals": "ownership-and-technicals.md",
    "working-capital-drivers": "working-capital-drivers.md",
    "core-drivers-summary": "core-drivers-summary.md",
    "qualitative-analysis-summary": "qualitative-analysis-summary.md",
    "revenue-drivers-forecast": "revenue-drivers-forecast.md",
    "gross-margin-drivers-forecast": "gross-margin-drivers-forecast.md",
    "operating-expenses-drivers-forecast": "operating-expenses-drivers-forecast.md",
    "net-income-drivers-forecast": "net-income-drivers-forecast.md",
    "unit-economics-drivers-forecast": "unit-economics-drivers-forecast.md",
    "drivers-forecast-summary": "drivers-forecast-summary.md",
    "working-capital-drivers-forecast": "working-capital-drivers-forecast.md",
    "balance-sheet-drivers-forecast": "balance-sheet-drivers-forecast.md",
    "leverage-and-cost-of-capital-drivers-forecast": "leverage-and-cost-of-capital-drivers-forecast.md",
    "roic-drivers-forecast": "roic-drivers-forecast.md",
    "fundamentals-forecast-summary": "fundamentals-forecast-summary.md",
    "revenue-growth-forecast": "revenue-growth-forecast.md",
    "gross-margin-forecast": "gross-margin-forecast.md",
    "operating-income-drivers-forecast": "operating-income-drivers-forecast.md",
    "net-income-drivers-financial-forecast": "net-income-drivers-financial-forecast.md",
    "shares-outstanding-and-eps-forecast": "shares-outstanding-and-eps-forecast.md",
    "working-capital-forecast": "working-capital-forecast.md",
    "capex-forecast": "capex-forecast.md",
    "free-cash-flow-forecast": "free-cash-flow-forecast.md",
    "exit-multiple-forecast": "exit-multiple-forecast.md",
    "dcf": "dcf.md",
    "valuation-summary": "valuation-summary.md",
    "report": "report.md",
    "report-summary": "report-summary.md",
    "price-target": "price-target.md",
    "trade-idea": "trade-idea.md",
}

def get_steps(ticker):
    doc = reports_collection.find_one({"company": ticker})
    if not doc:
        return []

    steps = doc.get("steps", {})
    if not isinstance(steps, dict):
        return []

    return list(steps.keys())

def get_prompt(step):
    path = "research/" + match_step_name_to_path[step]
    try:
        with open(path, "r") as f:
            data= f.read()
            return data
    except Exception as e:
        return "Could not find a relevent prompt!"


def get_output(ticker, step):
    doc = reports_collection.find_one(
    {"company": ticker},
    sort=[("created_at", DESCENDING)],
)
    if not doc:
        return "No document found for that company."

    steps = doc.get("steps", {})
    step = steps.get(step)

    return step["output"]


st.set_page_config(page_title="Prompt editing tool!", layout="wide")
st.title("Prompt editing tool!")

left, middle, right = st.columns(3)
prompt_middle = middle.container()
prompt_right = right.container()

with left:
    st.write("### Choose the company!")
    company = st.selectbox(
        "Tickers:",
        ['GEV', 'PLTR', 'COST', 'CVNA', 'CMG', 'AER', 'VST', 'ALAB', 'TMDX', 'OXY', 'AMD'],
    )

    steps = get_steps(company)

    if not steps:
        st.warning("No steps found for this company.")
    else:
        st.write("### Steps")
        for step in steps:
            if st.button(step):
                input = get_prompt(step)
                with prompt_middle:
                    st.write(f"### Prompt for {step}")
                    st.write(input)
                output = get_output(company, step)
                with prompt_right:
                    st.write(f"### Output for `{step}`")
                    st.write(output)
