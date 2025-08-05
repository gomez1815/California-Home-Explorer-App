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
    st.page_link("pages/Find_Ideal_Home.py", label="Find Ideal Home")
with col2:
    st.page_link("pages/Predict_Price.py", label = "Predict Home Price")
with col3:
    st.page_link("pages/Data_Sources.py", label = "Explore Data Sources")

# Additional Tools
col4, col5, col6, col7 = st.columns([1, 1, 1, 1])
with col5:
    st.page_link("pages/Investor.py", label = "For Investors")
with col6:
    st.page_link("pages/Data_Science.py", label = "For Data Scientists")

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

st.page_link("pages/Contact.py", label = "Contact")

st.markdown("---")
st.info("Built with Python, Streamlit, and real housing data. Powered by AI. © 2025 Taketo Horigome")
