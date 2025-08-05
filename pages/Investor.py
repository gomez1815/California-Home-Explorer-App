import streamlit as st

st.title("Investor Insights")

cols1, cols2 = st.columns([2,1])

with cols1:

    st.markdown("""
    ## California Real Estate Market Overview

    Discover investment opportunities across California using machine learning insights and market data.

    ---

    ### Key Trends
    - **Median Home Price Growth (5 Years):** +45%
    - **Top Performing Cities:** San Diego, Irvine, Oakland
    - **High Rent-to-Value Areas:** Fresno, Sacramento

    ---

    ## Investment Calculator

    Enter your parameters to estimate your ROI:
    """)

    purchase_price = st.number_input("Purchase Price ($)", min_value=1000, step=5000)
    monthly_rent = st.number_input("Monthly Rent ($)", min_value=100, step=100)
    annual_expenses = st.number_input("Annual Expenses ($)", min_value=100, step=100)

    if purchase_price > 0:
        gross_yield = (monthly_rent * 12) / purchase_price * 100
        net_yield = ((monthly_rent * 12) - annual_expenses) / purchase_price * 100

        st.markdown(f"""
        ### Results
        - **Gross Rental Yield:** `{gross_yield:.2f}%`
        - **Net Rental Yield:** `{net_yield:.2f}%`
        """)

    st.markdown("---")

    st.markdown("## Interested in collaborating?")
    st.page_link("pages/Contact.py", label = "Contact")


with cols2:
    st.image("https://images.unsplash.com/photo-1554224154-22dec7ec8818?auto=format&fit=crop&w=800&q=80", use_container_width=True)