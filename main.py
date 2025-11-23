import streamlit as st
import json

st.set_page_config("Terminal Prompt Editing Tool", layout="wide")
st.title("Terminal Prompt Editing Tool")

Core_drivers = [
    "Addressable market",
    "Revenue drivers",
    "Gross margin drivers",
    "Operating expenses drivers",
    "Net income drivers",
    "Working capital drivers",
    "Capital expenditure drivers",
    "Capital allocation drivers",
    "Capital structure drivers",
]

Fundamentals_forecast = [
    "Revenue forecast (4 quarters, 5 years)",
    "Gross profit forecast (4 quarters, 5 years)",
    "Operating income / loss forecast (4 quarters, 5 years)",
    "EBITDA & Net income forecast (4 quarters, 5 years)",
    "Cash flow from operations forecast",
    "Cash flow from investing forecast",
    "Cash flow from financing forecast",
    "Financial ratios forecast",
]

Core_drivers = [
    "Addressable market",
    "Revenue drivers",
    "Gross margin drivers",
    "Operating expenses drivers",
    "Net income drivers",
    "Working capital drivers",
    "Capital expenditure drivers",
    "Capital allocation drivers",
    "Capital structure drivers",
]

Fundamentals_forecast = [
    "Revenue forecast (4 quarters, 5 years)",
    "Gross profit forecast (4 quarters, 5 years)",
    "Operating income / loss forecast (4 quarters, 5 years)",
    "EBITDA & Net income forecast (4 quarters, 5 years)",
    "Cash flow from operations forecast",
    "Cash flow from investing forecast",
    "Cash flow from financing forecast",
    "Financial ratios forecast",
]

core_drivers_prompts = [
    "addressable-market-and-growth.md",        # Addressable market
    "revenue-drivers.md",                      # Revenue drivers
    "gross-margin-drivers.md",                 # Gross margin drivers
    "operating-expenses-drivers.md",           # Operating expenses drivers
    "net-income-drivers.md",                   # Net income drivers
    "working-capital-drivers.md",              # Working capital drivers
    "capex-forecast.md",                       # Capital expenditure drivers
    "roic-drivers.md",                         # Capital allocation drivers
    "leverage-and-cost-of-capital-drivers.md", # Capital structure drivers
]

fundamentals_forecast_prompts = [
    "revenue-drivers-forecast.md",                    # Revenue forecast
    "gross-margin-forecast.md",                       # Gross profit forecast
    "operating-income-drivers-forecast.md",           # Operating income / loss forecast
    "net-income-drivers-financial-forecast.md",       # EBITDA & Net income forecast
    "working-capital-forecast.md",                    # Cash flow from operations forecast
    "capex-forecast.md",                              # Cash flow from investing forecast
    "leverage-and-cost-of-capital-drivers-forecast.md", # Cash flow from financing forecast
    "roic-drivers-forecast.md",                       # Financial ratios forecast
]

left, middle, right = st.columns(3)

def write_prompt(prompt, name):
    with right:
        st.write("# Prompt for: ", name)
        st.write(prompt)



with left:
    st.write("# Drivers")
    for i , driver in enumerate(Core_drivers):
        if st.button(driver):
            name = core_drivers_prompts[i]
            path = "research/" + name
            with open(path, "r") as f:
                data= f.read()
            write_prompt(data, driver)

with middle:
    st.write("# Fundamental Forecast")
    for i , forecast in enumerate(Fundamentals_forecast):
            if st.button(forecast):
                name =fundamentals_forecast_prompts[i]
                path = "research/" + name
                with open(path, "r") as f:
                    data= f.read()
                write_prompt(data, driver)