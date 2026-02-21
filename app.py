import streamlit as st
import math
from datetime import datetime

# -------------------------
# App Title
# -------------------------

st.set_page_config(page_title="Epidemiology Metrics Calculator", layout="centered")

st.title("🦠 Epidemiology Metrics Calculator")
st.write("Interactive tool for surveillance and outbreak response analysis.")

# -------------------------
# Session State for History
# -------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Sidebar Menu
# -------------------------

metric = st.sidebar.selectbox(
    "Select Metric",
    [
        "Attack Rate",
        "Case Fatality Rate (CFR)",
        "Incidence Rate",
        "Prevalence",
        "Doubling Time"
    ]
)

st.header(metric)

# -------------------------
# Calculations
# -------------------------

def record_result(name, value, unit=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"[{timestamp}] {name}: {round(value,2)} {unit}"
    st.session_state.history.append(record)


if metric == "Attack Rate":
    cases = st.number_input("New cases", min_value=0.0)
    population = st.number_input("Population at risk", min_value=0.0)

    if st.button("Calculate Attack Rate"):
        if population > 0:
            result = (cases / population) * 100
            st.success(f"Attack Rate: {round(result,2)} %")
            record_result("Attack Rate (%)", result, "%")
        else:
            st.error("Population must be greater than zero.")

elif metric == "Case Fatality Rate (CFR)":
    deaths = st.number_input("Number of deaths", min_value=0.0)
    cases = st.number_input("Confirmed cases", min_value=0.0)

    if st.button("Calculate CFR"):
        if cases > 0:
            result = (deaths / cases) * 100
            st.success(f"CFR: {round(result,2)} %")
            record_result("CFR (%)", result, "%")
        else:
            st.error("Cases must be greater than zero.")

elif metric == "Incidence Rate":
    cases = st.number_input("New cases", min_value=0.0)
    population = st.number_input("Total population", min_value=0.0)
    multiplier = st.number_input("Multiplier (e.g., 1000 or 100000)", min_value=1.0)

    if st.button("Calculate Incidence Rate"):
        if population > 0:
            result = (cases / population) * multiplier
            st.success(f"Incidence Rate: {round(result,2)}")
            record_result("Incidence Rate", result)
        else:
            st.error("Population must be greater than zero.")

elif metric == "Prevalence":
    existing_cases = st.number_input("Existing cases", min_value=0.0)
    population = st.number_input("Total population", min_value=0.0)

    if st.button("Calculate Prevalence"):
        if population > 0:
            result = (existing_cases / population) * 100
            st.success(f"Prevalence: {round(result,2)} %")
            record_result("Prevalence (%)", result, "%")
        else:
            st.error("Population must be greater than zero.")

elif metric == "Doubling Time":
    growth_rate = st.number_input("Exponential growth rate (e.g., 0.2)", min_value=0.0001)

    if st.button("Calculate Doubling Time"):
        result = math.log(2) / growth_rate
        st.success(f"Doubling Time: {round(result,2)} days")
        record_result("Doubling Time (days)", result, "days")

# -------------------------
# History Section
# -------------------------

st.markdown("---")
st.subheader("📜 Calculation History")

if st.session_state.history:
    for item in st.session_state.history:
        st.write(item)
else:
    st.write("No calculations yet.")