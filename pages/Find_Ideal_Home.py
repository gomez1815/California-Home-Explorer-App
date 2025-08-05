# Find_Ideal_Home.py

import streamlit as st
import pandas as pd
from background import set_background

final_df = pd.read_csv("final_df.csv")


st.title("Find Your Ideal Home")

final_df = final_df.rename(columns = {'UnparsedAddress_x': 'Address',
                                      'ClosePrice_y': 'Price'})


col1, col2 = st.columns([2,1])

with col1:

    st.markdown("### Find Your Ideal Home")

    max_budget = st.number_input("Enter your maximum budget (USD):", value=0)
    min_beds = st.number_input("Minimum number of bedrooms:", min_value=0, value=1)
    min_baths = st.number_input("Minimum number of bathrooms:", min_value=0, value=1)
    min_area = st.number_input("Minimum living area (sqft):", min_value=0, value=1)
        
    if st.button("Show Matching Properties"):

        matching_homes = final_df[
            (final_df['Price'] <= max_budget) &
            (final_df['BedroomsTotal'] >= min_beds) &
            (final_df['BathroomsTotalInteger'] >= min_baths) &
            (final_df['LivingArea'] >= min_area)
        ]

        if not matching_homes.empty:
            st.success(f"Found {len(matching_homes)} matching homes")

            top_n = min(len(matching_homes), 10)

            if top_n > 0:
                # Sort and select top N
                top_homes = matching_homes.sort_values(by='Price').head(top_n)
                
                # Display as table
                st.dataframe(top_homes[['Address', 'City', 'Price']])

                # Map (remember to rename lat/lon)
                map_df = top_homes.rename(columns={
                    'Latitude': 'latitude',
                    'Longitude': 'longitude'
                })

                st.markdown(f"### Top {top_n} Most Ideal Home{'s' if top_n > 1 else ''} Location")
                st.map(map_df[['latitude', 'longitude']], zoom=11)
            else:
                st.warning("No matching homes found.")


with col2:
    st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994", use_container_width=True)