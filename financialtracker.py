import streamlit as st
import pandas as pd
import altair as alt

# Set the app layout and title
st.set_page_config(page_title="Utility Offset Calculator", layout="wide")
st.title("Utility Expense Offset Calculator")

# Projection period selection
years = st.slider("Projection Period (Years)", min_value=1, max_value=30, value=10)

# Investment Details Section
st.write("### Investment Details")
col1, col2, col3 = st.columns(3)
investment_amount = col1.number_input("Investment Amount ($)", min_value=0.0, value=0.0)
annual_roi = col2.number_input("Annual Return on Investment (%)", min_value=0.0, value=10.0)
tax_rate = col3.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=0.0)

# Calculate Post-Tax ROI Using Tax Rate
if tax_rate > 0:
    annual_gain = investment_amount * (annual_roi / 100)
    tax_amount = annual_gain * (tax_rate / 100)
    post_tax_gain = annual_gain - tax_amount
    post_tax_roi = (post_tax_gain / investment_amount) * 100
else:
    post_tax_roi = annual_roi

# Calculate Investment Coverage Over Time with post-tax ROI
investment_value = investment_amount * (1 + post_tax_roi / 100) ** years

# Initialize utilities with a default utility
if "utilities" not in st.session_state:
    st.session_state.utilities = [{"name": "Electricity", "monthly_cost": 35.0, "inflation_rate": 3.0}]

# Button to add a new utility
if st.button("Add Utility Bill"):
    st.session_state.utilities.append({"name": "", "monthly_cost": 0.0, "inflation_rate": 3.0})

# Display input fields for each utility bill in the list
for idx, utility in enumerate(st.session_state.utilities):
    st.write(f"Utility Bill {idx + 1}")
    utility["name"] = st.text_input(f"Utility Name {idx + 1}", value=utility["name"], key=f"name_{idx}")
    utility["monthly_cost"] = st.number_input(f"Monthly Cost for {utility['name']} ($)", value=utility["monthly_cost"], key=f"cost_{idx}")
    utility["inflation_rate"] = st.number_input(f"Inflation Rate for {utility['name']} (%)", value=utility["inflation_rate"], key=f"inflation_{idx}")

# Update utility data to check if fully covered by investment
utility_data = []
for utility in st.session_state.utilities:
    total_annual_cost = utility["monthly_cost"] * 12
    is_covered = investment_value >= total_annual_cost
    utility_data.append({
        "Utility": utility["name"],
        "Annual Cost": total_annual_cost,
        "Covered": "✓" if is_covered else "✗",
        "Color": "green" if is_covered else "blue"
    })

# Create DataFrame for visualization
chart_data = pd.DataFrame(utility_data)

# Display Utility Expense Pie Chart with checkmarks for covered utilities
st.write("### Utility Expense Coverage")
pie_chart = alt.Chart(chart_data).mark_arc().encode(
    theta=alt.Theta(field="Annual Cost", type="quantitative"),
    color=alt.Color('Color', scale=None, legend=None),
    tooltip=["Utility", "Annual Cost", "Covered"]
).properties(width=300, height=300)

st.altair_chart(pie_chart)
st.write("Utilities marked in **green** with a checkmark (✓) are fully covered by your investment.")

# Display utility details in a table format with coverage status
st.write("### Utility Coverage Summary")
st.dataframe(chart_data[["Utility", "Annual Cost", "Covered"]])

# Display Effective ROI (either post-tax or original based on input)
if tax_rate > 0:
    st.write(f"### Effective Post-Tax ROI: {post_tax_roi:.2f}%")
else:
    st.write(f"### ROI (No Tax Applied): {post_tax_roi:.2f}%")

# Display Total Projected Investment Value After Tax
st.write("### Total Projected Investment Value")
st.write(f"With a starting investment of ${investment_amount:,.2f} and an effective ROI of {post_tax_roi:.2f}%:")
st.metric(label=f"Total Investment Value after {years} Years", value=f"${investment_value:,.2f}")

# Final message about overall coverage for the selected years
if all(utility["Color"] == "green" for utility in utility_data):
    st.success("Your investment covers all utility expenses for the selected period!")
else:
    st.warning("Your investment does not fully cover all utility expenses.")
