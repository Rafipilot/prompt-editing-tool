import streamlit as st
from dotenv import load_dotenv
import os
from pymongo import MongoClient, DESCENDING

from runCustomPrompt import run_custom_prompt

load_dotenv()

mongo_uri = os.environ["MONGODB_URI"]
client = MongoClient(mongo_uri)

db = client["companies"]
reports_collection = db["company_research_reports"]


match_step_name_to_path = {
    "company-research": "company-research.md",
    "qualitative-analysis": "qualitative-analysis.md",
    "core-drivers": "core-drivers.md",
    "competition": "competition.md",
    "industry-and-strategy-context": "industry-and-strategy-context.md",
    "defensibility-and-moats": "defensibility-and-moats.md",
    "m&a-and-being-acquired": "m&a-and-being-acquired.md",
    "addressable-market-and-growth": "addressable-market-and-growth.md",
    "ownership-and-technicals": "ownership-and-technicals.md",
    "cyclicality": "cyclicality.md",
    "product-highlights": "product-highlights.md",
    "capital-allocation-drivers": "capital-allocation-drivers.md",
    "management-team": "management-team.md",
    "gross-margin-drivers": "gross-margin-drivers.md",
    "net-income-drivers": "net-income-drivers.md",
    "capital-expenditure-drivers": "capital-expenditure-drivers.md",
    "revenue-drivers": "revenue-drivers.md",
    "customer-profile-and-customer-concentration": "customer-profile-and-customer-concentration.md",
    "operating-expenses-drivers": "operating-expenses-drivers.md",
    "business-model": "business-model.md",
    "long-term-growth": "long-term-growth.md",
    "working-capital-drivers": "working-capital-drivers.md",
    "capital-structure-drivers": "capital-structure-drivers.md",
    "attractiveness-of-end-market": "attractiveness-of-end-market.md",
    "product-value-add-and-pricing-power": "product-value-add-and-pricing-power.md",
    "qualitative-analysis-summary": "qualitative-analysis-summary.md",
    "core-drivers-summary": "core-drivers-summary.md",
    "revenue-forecast": "revenue-forecast.md",
    "gross-profit-forecast": "gross-profit-forecast.md",
    "operating-income-loss-forecast": "operating-income-loss-forecast.md",
    "ebitda-and-net-income-forecast": "ebitda-and-net-income-forecast.md",
    "cash-flow-from-operations-forecast": "cash-flow-from-operations-forecast.md",
    "cash-flow-from-investing-forecast": "cash-flow-from-investing-forecast.md",
    "cash-flow-from-financing-forecast": "cash-flow-from-financing-forecast.md",
    "financial-forecast": "financial-forecast.md",
    "report": "report.md",
    "report-summary": "report-summary.md",
    "price-target": "price-target.md",
    "trade-idea": "trade-idea.md",
    "report-update-comparison": "report-update-comparison.md",
    "report-comparison-summary": "report-comparison-summary.md",
}

def get_steps(ticker):
    doc = reports_collection.find_one(
    {"company": ticker},
    sort=[("created_at", DESCENDING)],
)
    if not doc:
        return []

    steps = doc.get("steps", {})
    if not isinstance(steps, dict):
        return []

    return list(steps.keys())

def get_prompt(step, company: str):
    path = "research/" + match_step_name_to_path[step]
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()

        return data.format(company=company)

    except FileNotFoundError:
        print(f"Prompt file not found at: {path}")
        return "Could not find a relevant prompt!"
    except Exception as e:
        print(f"Error loading prompt for step {step}: {e}")
        return "Could not find a relevant prompt!"


def get_output(ticker, step):
    doc = reports_collection.find_one(
    {"company": ticker},
    sort=[("created_at", DESCENDING)],
)
    if not doc:
        return "No document found for that company."

    steps = doc.get("steps", {})
    step = steps.get(step)

    return step.get("output", "No output found")


st.set_page_config(page_title="Prompt editing tool!", layout="wide")


if "edit_selected_step" not in st.session_state:
    st.session_state["edit_selected_step"] = None
if "edit_selected_company" not in st.session_state:
    st.session_state["edit_selected_company"] = None

st.title("Prompt editing tool!")

tab1, tab2 = st.tabs(["View Current Prompt/ Outputs", "Edit prompts and generate new outputs"])


with tab1:
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
                if st.button(step, key=f"view_{step}"):
                    input_text = get_prompt(step, company)
                    with prompt_middle:
                        st.write(f"### Prompt for {step}")
                        st.write(input_text)
                    output = get_output(company, step)
                    with prompt_right:
                        st.write(f"### Output for `{step}`")
                        st.write(output)
with tab2:
    left, middle, right = st.columns(3)
    prompt_middle = middle.container()
    prompt_right = right.container()

    with left:
        st.write("### Choose the company! ")
        company = st.selectbox(
            "Tickerz:",
            ['GEV', 'PLTR', 'COST', 'CVNA', 'CMG', 'AER', 'VST', 'ALAB', 'TMDX', 'OXY', 'AMD'],
            key="company_edit",
        )

        # If company changes, reset selected step
        if st.session_state["edit_selected_company"] != company:
            st.session_state["edit_selected_company"] = company
            st.session_state["edit_selected_step"] = None

        steps = get_steps(company)

        if not steps:
            st.warning("No steps found for this company.")
        else:
            st.write("### Steps")
            for step in steps:
                if st.button(step, key=f"edit_{company}_{step}"):
                    st.session_state["edit_selected_step"] = step

    selected_step = st.session_state.get("edit_selected_step")

    if selected_step:
        # Load the prompt for the selected step
        input_text = get_prompt(selected_step, company)

        with prompt_middle:
            st.write(f"### Current prompt for {selected_step}")
            edited_prompt = st.text_area(
                "Edit prompt",
                value=input_text,
                height=800,
                key=f"prompt_{company}_{selected_step}",
            )

            if st.button("Try prompt", key=f"try_{company}_{selected_step}"):
                with prompt_right:
                    with st.spinner("Generating output..."):
                        # use the latest value from the text_area
                        output = run_custom_prompt(
                            company=company,
                            model="gpt-4-turbo",
                            prompt=edited_prompt,
                            step_name=selected_step,  # optional, metadata
                        )
                        st.write("### Edited Prompt response: ")
                        st.write(output)

            if st.button("Save prompt", key=f"save_prompt_{company}_{selected_step}"):
                # update_prompt(company, selected_step, edited_prompt)
                st.success("Prompt saved")

        # Always show the last stored output from Mongo
        output = get_output(company, selected_step)
        with prompt_right:
            st.write(f"### Output for `{selected_step}`")
            st.write(output)
    else:
        with prompt_middle:
            st.info("Select a step on the left to edit its prompt.")
