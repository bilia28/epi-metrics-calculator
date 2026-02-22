# =========================================================
# OUTBREAK RAPID ANALYSIS TOOL (HYBRID VERSION - STABLE)
# =========================================================

import streamlit as st
import pandas as pd
import math
from datetime import datetime
import io

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Outbreak Rapid Analysis Tool",
    layout="centered"
)

st.title("🦠 Outbreak Rapid Analysis Tool")
st.write("District-level surveillance and rapid outbreak analysis dashboard.")

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

def record_result(name, value, unit=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"[{timestamp}] {name}: {round(value,2)} {unit}"
    st.session_state.history.append(record)

# ---------------------------------------------------------
# SIDEBAR MODE
# ---------------------------------------------------------

st.sidebar.title("Dashboard Mode")

app_mode = st.sidebar.radio(
    "Select Mode",
    ["Academic Version (Free)", "NGO Version (Premium)"]
)

# ---------------------------------------------------------
# DATASET UPLOAD
# ---------------------------------------------------------

st.markdown("---")
st.header("📂 Upload Surveillance Dataset")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

df = None
df_filtered = None

if uploaded_file is not None:

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Dataset uploaded successfully.")
        st.write("Preview:")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

# ---------------------------------------------------------
# FILTER SECTION
# ---------------------------------------------------------

if df is not None:

    st.markdown("---")
    st.header("🔎 Data Filters")

    df_filtered = df.copy()

    # --- DATE FILTER ---
    if "date" in df_filtered.columns:
        try:
            df_filtered["date"] = pd.to_datetime(df_filtered["date"], errors="coerce")
            df_filtered = df_filtered.dropna(subset=["date"])

            start_date = st.date_input(
                "Start Date",
                value=df_filtered["date"].min()
            )

            end_date = st.date_input(
                "End Date",
                value=df_filtered["date"].max()
            )

            df_filtered = df_filtered[
                (df_filtered["date"] >= pd.to_datetime(start_date)) &
                (df_filtered["date"] <= pd.to_datetime(end_date))
            ]

        except Exception as e:
            st.warning("Date column found but could not process properly.")

    # --- LOCATION FILTER ---
    if "location" in df_filtered.columns:
        locations = df_filtered["location"].dropna().unique()
        location_filter = st.multiselect("Select Location", locations)

        if location_filter:
            df_filtered = df_filtered[
                df_filtered["location"].isin(location_filter)
            ]

    # --- AGE GROUP FILTER ---
    if "age_group" in df_filtered.columns:
        age_groups = df_filtered["age_group"].dropna().unique()
        age_filter = st.multiselect("Select Age Group", age_groups)

        if age_filter:
            df_filtered = df_filtered[
                df_filtered["age_group"].isin(age_filter)
            ]

    st.subheader("Filtered Data")
    st.dataframe(df_filtered)

# ---------------------------------------------------------
# EPIDEMIC CURVE
# ---------------------------------------------------------

if df_filtered is not None and "date" in df_filtered.columns:

    st.markdown("---")
    st.header("📈 Epidemic Curve (By Epidemiological Week)")

    try:
        df_temp = df_filtered.copy()
        df_temp["epi_week"] = df_temp["date"].dt.isocalendar().week

        weekly_cases = (
            df_temp.groupby("epi_week")
            .size()
            .reset_index(name="cases")
            .sort_values("epi_week")
        )

        if not weekly_cases.empty:
            st.line_chart(
                weekly_cases.set_index("epi_week")["cases"]
            )
        else:
            st.info("No data available for selected filters.")

    except Exception as e:
        st.warning("Could not generate epidemic curve.")

# ---------------------------------------------------------
# EXPORT SECTION
# ---------------------------------------------------------

if df_filtered is not None and not df_filtered.empty:

    st.markdown("---")
    st.header("⬇ Download Filtered Data")

    try:
        output = io.BytesIO()
        df_filtered.to_excel(output, index=False)

        st.download_button(
            label="Download as Excel",
            data=output.getvalue(),
            file_name="filtered_surveillance_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception:
        st.warning("Excel export requires openpyxl. Install using: pip install openpyxl")

# ---------------------------------------------------------
# METRIC CALCULATOR
# ---------------------------------------------------------

st.markdown("---")
st.header("🧮 Epidemiology Metrics Calculator")

metric = st.selectbox(
    "Select Metric",
    [
        "Attack Rate",
        "Case Fatality Rate (CFR)",
        "Incidence Rate",
        "Prevalence",
        "Doubling Time"
    ]
)

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
    growth_rate = st.number_input(
        "Exponential growth rate (e.g., 0.2)",
        min_value=0.0001
    )

    if st.button("Calculate Doubling Time"):
        result = math.log(2) / growth_rate
        st.success(f"Doubling Time: {round(result,2)} days")
        record_result("Doubling Time (days)", result, "days")

# ---------------------------------------------------------
# HISTORY
# ---------------------------------------------------------

st.markdown("---")
st.subheader("📜 Calculation History")

if st.session_state.history:
    for item in st.session_state.history:
        st.write(item)
else:
    st.write("No calculations yet.")