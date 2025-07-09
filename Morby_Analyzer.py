import streamlit as st

def inject_dm_sans():
    st.markdown("""
                <style>
                @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap');

        html, body, [class*="css"]  {
            font-family: 'DM Sans', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

inject_dm_sans()

st.set_page_config(page_title="Morby Method Deal Analyzer", layout="centered")

st.title("🏡 Morby Method Deal Analyzer")
st.caption("Use a DSCR loan + seller finance + transactional funds to acquire real estate with 100% financing.")

# Input Section
st.header("🔢 Deal Inputs")

col1, col2 = st.columns(2)
with col1:
    purchase_price = st.number_input("Purchase Price ($)", value=0)
    market_rent = st.number_input("Monthly Market Rent ($)", value=0)
    closing_costs = st.number_input("Estimated Closing Costs ($)", value=0)
    max_ltv_pct = st.slider("Max LTV % for DSCR Loan", 50, 90, 75)

with col2:
    dscr_ratio = st.number_input("DSCR Requirement", value=1.15)
    dscr_interest = st.number_input("DSCR Interest Rate (%)", value=8.25) / 100
    dscr_years = st.number_input("DSCR Loan Term (Years)", value=30)
    transactional_fee_pct = st.number_input("Transactional Lender Fee (%)", value=2.0) / 100

st.divider()
st.header("💰 Seller Finance Terms")

col3, col4 = st.columns(2)
with col3:
    seller_interest = st.number_input("Seller Finance Interest Rate (%)", value=5) / 100
with col4:
    seller_years = st.number_input("Seller Finance Amortization (Years)", value=30)

# --- Calculations ---
# DSCR loan by rent support
monthly_dscr_payment = market_rent / dscr_ratio
dscr_monthly_rate = dscr_interest / 12
dscr_n = dscr_years * 12

if dscr_monthly_rate == 0:
    rent_based_dscr_loan = monthly_dscr_payment * dscr_n
else:
    rent_based_dscr_loan = monthly_dscr_payment * ((1 - (1 + dscr_monthly_rate) ** -dscr_n) / dscr_monthly_rate)

# DSCR loan by LTV
ltv_based_dscr_loan = purchase_price * (max_ltv_pct / 100)
dscr_loan_amount = min(rent_based_dscr_loan, ltv_based_dscr_loan)

# Seller finance gap
seller_finance_amount = purchase_price - dscr_loan_amount

# Seller monthly payment (amortized)
seller_monthly_rate = seller_interest / 12
seller_n = seller_years * 12
if seller_monthly_rate == 0:
    seller_monthly_payment = seller_finance_amount / seller_n
else:
    seller_monthly_payment = seller_finance_amount * (seller_monthly_rate * (1 + seller_monthly_rate) ** seller_n) / ((1 + seller_monthly_rate) ** seller_n - 1)

# DSCR monthly payment (amortized)
if dscr_monthly_rate == 0:
    dscr_monthly_payment = dscr_loan_amount / dscr_n
else:
    dscr_monthly_payment = dscr_loan_amount * (dscr_monthly_rate * (1 + dscr_monthly_rate) ** dscr_n) / ((1 + dscr_monthly_rate) ** dscr_n - 1)

# Total debt and cash flow
total_monthly_debt = dscr_monthly_payment + seller_monthly_payment
monthly_cash_flow = market_rent - total_monthly_debt

# Transactional funding
transactional_base = seller_finance_amount + closing_costs
transactional_fee = transactional_base * transactional_fee_pct
transactional_repay = transactional_base + transactional_fee

# --- Output ---
st.divider()
st.header("📊 Deal Summary")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("DSCR Loan Amount", f"${dscr_loan_amount:,.2f}")
with col2:
    st.metric("Seller Finance Amount", f"${seller_finance_amount:,.2f}")
with col3:
    st.metric("Monthly Rent", f"${market_rent:,.2f}")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("DSCR Payment", f"${dscr_monthly_payment:,.2f}")
with col5:
    st.metric("Seller Payment", f"${seller_monthly_payment:,.2f}")
with col6:
    st.metric("Total Debt", f"${total_monthly_debt:,.2f}")

col7, col8, col9 = st.columns(3)
with col7:
    st.metric("Cash Flow", f"${monthly_cash_flow:,.2f}")
with col8:
    st.metric("Closing Costs", f"${closing_costs:,.2f}")
with col9:
    st.metric("DSCR Ratio", f"{dscr_ratio:.2f}x")

# Transactional Funding Section
st.divider()
st.subheader("💼 Transactional Funding")

st.write(f"**Required Funds (Seller Note + Closing)**: ${transactional_base:,.2f}")
st.write(f"**Lender Fee @ {transactional_fee_pct * 100:.1f}%**: ${transactional_fee:,.2f}")
st.write(f"**Total Repayment to Transactional Lender**: ${transactional_repay:,.2f}")
