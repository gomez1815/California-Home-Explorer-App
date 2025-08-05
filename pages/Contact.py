import streamlit as st

st.title("Contact")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Contact Information

    - **Developer**: Taketo Horigome  
    - **Email**: [liverdom@icloud.com](mailto:liverdom@icloud.com)  
    - **GitHub**: [github.com/gomez1815](https://github.com/gomez1815)  
    - **LinkedIn**: [linkedin.com/in/taketo-horigome](https://www.linkedin.com/in/taketo-horigome-29b26532b/)  
    """)

with col2:
    st.image("https://images.unsplash.com/photo-1519389950473-47ba0277781c", use_container_width=True)

st.markdown("---")
