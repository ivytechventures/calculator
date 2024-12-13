import streamlit as st

# App Title
st.title("Bill Offset Calculator")
st.write("""
This prototype helps you determine the total amount you need to save or invest 
to cover your recurring expenses forever, based on an expected annual return rate.
""")

# Input Fields
monthly_bill = st.number_input("Enter your monthly bill amount ($):")
expected_return_rate = st.number_input("Enter the expected annual return rate (%):")
inflation_rate = st.number_input("Enter the annual inflation rate (%):", min_value=0.0, max_value=100.0, step=0.1, value=0.0)
tax_rate = st.number_input("Enter the tax rate on investment returns (%):", min_value=0.0, max_value=100.0, step=0.1, value=0.0)

# Calculate Required Investment and Taxes
if monthly_bill > 0 and expected_return_rate > 0:
    # Step 1: Calculate the annual bill
    annual_bill = monthly_bill * 12
    
    # Step 2: Adjust for inflation
    inflation_adjusted_annual_bill = annual_bill * (1 + inflation_rate / 100)
    
    # Step 3: Calculate taxes on withdrawals
    tax_on_withdrawal = inflation_adjusted_annual_bill * (tax_rate / 100)
    
    # Step 4: Calculate the required investment (before and after tax)
    required_investment_before_tax = inflation_adjusted_annual_bill / (expected_return_rate / 100)
    required_investment_after_tax = (inflation_adjusted_annual_bill + tax_on_withdrawal) / (expected_return_rate / 100)
    
    # Display Results
    st.write(f"### Annual Bill: ${annual_bill:.2f}")
    st.write(f"### Inflation-Adjusted Annual Bill: ${inflation_adjusted_annual_bill:.2f}")
    st.write(f"### Required Investment (before tax): ${required_investment_before_tax:.2f}")
    st.write(f"### Taxes on Withdrawal (at {tax_rate}%): ${tax_on_withdrawal:.2f}")
    st.write(f"### Required Investment (after tax): ${required_investment_after_tax:.2f}")
else:
    st.write("Please enter valid values for your monthly bill, expected return rate, inflation rate, and tax rate.")
    
# Footer
st.write("---")
st.write("Built by The Ivys")
