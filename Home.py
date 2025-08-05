import streamlit as st
from background import set_background  


# App Title and Tagline
st.title("California Home Explorer")
st.caption("Your one-stop destination to explore, analyze, and predict California real estate.")

# Hero Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## Welcome to Your Real Estate Playground!

    Explore California homes, uncover hidden gems,  
    and use AI to **predict home prices** with just a few clicks.

    Whether you're a buyer, seller, investor, or simply curious –  
    **this tool is made for you.**
    """)
    st.markdown("Select a feature below or use the sidebar to begin.")

with col2:
    st.image(
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
        use_container_width=True
    )

# Divider
st.markdown("---")

# Feature Navigation Buttons
st.subheader("Explore App Features")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Find Ideal Home"):
        st.switch_page("pages/Find_Ideal_Home.py")
with col2:
    if st.button("Predict Home Price"):
        st.switch_page("pages/Predict_Price.py")
with col3:
    if st.button("Explore Data Sources"):
        st.switch_page("pages/Data_Sources.py")

# Additional Tools
col4, col5, col6, col7 = st.columns([1, 1, 1, 1])
with col5:
    if st.button("For Investors"):
        st.switch_page("pages/Investor.py")
with col6:
    if st.button("For Data Scientists"):
        st.switch_page("pages/Data_Science.py")

# Explanation Section
with st.expander("How This App Works"):
    st.markdown("""
    - Use the sidebar or buttons to explore app sections  
    - Enter property details or preferences  
    - Let the AI model estimate home prices  
    - Analyze trends by distance to coast or city  
    - Browse clean documentation of data and methods  
    """)

# Divider
st.markdown("---")

# Footer + Contact
st.markdown("## Let's Connect!")
st.markdown("Have questions, feedback, or want to collaborate?")

if st.button("Click here to get in touch"):
    st.switch_page("pages/Contact.py")

st.markdown("---")
st.info("Built with Python, Streamlit, and real housing data. Powered by AI. © 2025 Taketo Horigome")
