import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import io
import time
from math import radians, cos, sin, asin, sqrt
from fpdf import FPDF
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from background import set_background

# Set background


st.title("Predict Home Price")

cols1, cols2 = st.columns([2,1])

with cols1:

    # Load all models & files
    model = joblib.load("pkl/xgb_home_price_model.pkl")
    features = joblib.load("pkl/model_features.pkl")
    top_100_expensive_cities = joblib.load("pkl/top_100_expensive_cities.pkl")
    top_100_cheap_cities = joblib.load("pkl/top_100_cheap_cities.pkl")
    top_20_famous_cities = joblib.load("pkl/top_20_famous_cities.pkl")
    living_area_thresh = joblib.load("pkl/living_area_thresh.pkl")
    room_thresh = joblib.load("pkl/room_thresh.pkl")
    small_area_thresh = joblib.load("pkl/small_area_thresh.pkl")
    kmeans = joblib.load("pkl/location_kmeans.pkl")
    density_thresh = joblib.load("pkl/room_density_thresh.pkl")
    cheap_volume_cities = joblib.load("pkl/cheap_high_volume_cities.pkl")

    # Safe geocoder
    def safe_geocode(geolocator, address, max_retries=3):
        for i in range(max_retries):
            try:
                return geolocator.geocode(address, addressdetails=True, timeout=10)
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                st.warning(f"Geocoding attempt {i+1} failed: {e}")
                time.sleep(2)
        st.error("Failed to geocode address. Please try again later.")
        return None

    # Distance logic
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        return R * 2 * np.arcsin(np.sqrt(a))

    def find_closest_place(user_lat, user_lon, places):
        closest = min(places, key=lambda x: haversine_distance(user_lat, user_lon, *x[1]))
        return closest[0], haversine_distance(user_lat, user_lon, *closest[1])

    # Geolocation
    geolocator = Nominatim(user_agent="home_price_app")
    address_input = st.text_input("Enter Full Address")
    if not address_input:
        st.stop()

    location = safe_geocode(geolocator, address_input)
    if not location:
        st.stop()

    latitude = location.latitude
    longitude = location.longitude
    full_address = location.address
    address_data = location.raw.get("address", {})
    city_name = (
        address_data.get("city") or address_data.get("town") or address_data.get("village") or
        address_data.get("municipality") or address_data.get("city_district") or
        address_data.get("suburb") or address_data.get("county") or address_data.get("state")
    )
    st.success(f"Found: {full_address}")
    st.map(pd.DataFrame([{'latitude': latitude, 'longitude': longitude}]), zoom=12)

    coastal_points = [
        ("Crescent City", (41.7558, -124.2026)),
        ("Eureka", (40.8021, -124.1637)),
        ("Mendocino", (39.3075, -123.7995)),
        ("San Francisco", (37.7599, -122.5107)),
        ("Santa Cruz", (36.9741, -122.0308)),
        ("Monterey", (36.6002, -121.8947)),
        ("Pismo Beach", (35.1428, -120.6413)),
        ("Santa Barbara", (34.4208, -119.6982)),
        ("Santa Monica", (34.0195, -118.4912)),
        ("San Diego", (32.8328, -117.2713)),
    ]


    major_centers = [
        ("Los Angeles", (34.0522, -118.2437)),
        ("San Francisco", (37.7749, -122.4194)),
        ("San Diego", (32.7157, -117.1611)),
        ("Sacramento", (38.5816, -121.4944)),
        ("San Jose", (37.3382, -121.8863)),
        ("Fresno", (36.7378, -119.7871))
    ]

    closest_coast, distance_to_coast = find_closest_place(latitude, longitude, coastal_points)
    closest_downtown, distance_to_downtown = find_closest_place(latitude, longitude, major_centers)

    st.info(f"Closest Beach ({closest_coast}): {distance_to_coast:.1f} km")
    st.info(f"Closest Downtown ({closest_downtown}): {distance_to_downtown:.1f} km")

    # User input
    floors = st.slider("Floors", 0, 10, 1)
    bedrooms = st.slider("Bedrooms", 0, 10, 3)
    bathrooms = st.slider("Bathrooms", 0, 10, 2)
    living_area = st.number_input("Living Area (sq ft)", 1, 10000, 1500)
    lot_size = st.number_input("Lot Size (sq ft)", 1, 100000, 5000)
    year_built = st.number_input("Year Built", 1800, 2025, 2005)
    pool = st.checkbox("Has Pool")
    fireplace = st.checkbox("Has Fireplace")
    garage = st.checkbox("Has Garage")

    # Derived features
    age = 2025 - year_built
    is_new = int(year_built >= 2020)
    total_rooms = bedrooms + bathrooms
    lot_per_living = lot_size / living_area
    rooms_per_area = total_rooms / living_area
    bedbath_ratio = bedrooms / bathrooms if bathrooms else 0
    bath_per_room = bathrooms / total_rooms
    has_fireplace = int(fireplace)
    has_garage = int(garage)
    pool_false = int(not pool)

    input_dict = {
        'LivingArea': living_area,
        'BathroomsTotalInteger': bathrooms,
        'BedroomsTotal': bedrooms,
        'LotSizeSquareFeet': lot_size,
        'LargeLivingArea_With_EnoughRoom': int(living_area > living_area_thresh and total_rooms > room_thresh),
        'LotPerLivingArea': lot_per_living,
        'Has_Fireplace': has_fireplace,
        'Is_New': is_new,
        'distance_to_downtown': distance_to_downtown,
        'Levels_Clean': 3 if floors > 3 else floors,
        'Latitude': latitude,
        'Longitude': longitude,
        'YearBuilt': year_built,
        'LocationCluster': int(kmeans.predict([[latitude, longitude]])[0]),
        'HasGarage': has_garage,
        'PoolPrivateYN_False': pool_false,
        'TotalRooms': total_rooms,
        'TotalRoomsPerLivingArea': rooms_per_area,
        'ExpensiveCity': int(city_name in top_100_expensive_cities),
        'FamousCity_With_LargeHouse': int(city_name in top_20_famous_cities and living_area > living_area_thresh),
        'ExpensiveCity_With_LargeHouse': int(city_name in top_100_expensive_cities and living_area > living_area_thresh),
        'Age': age,
        'Pool&Fireplace': int(pool and fireplace),
        'NewinExpensiveCity': int(is_new and city_name not in top_100_expensive_cities),
        'BedBathRatio': bedbath_ratio,
        'BathPerRoom': bath_per_room,
        'ExpensiveCitywithPool': int(city_name in top_100_expensive_cities and pool),
        'DistanceToCoast_km': distance_to_coast,
        'CheapCity': int(city_name in top_100_cheap_cities),
        'CheapHighVolumeCity': int(city_name in cheap_volume_cities),
        'HighRoomDensity': int(rooms_per_area > density_thresh),
        'SmallLivingArea': int(living_area < small_area_thresh)
    }

    input_df = pd.DataFrame([input_dict])[features]

    # Predict
    if st.button("Predict Home Price"):
        price = model.predict(input_df)[0]
        mape = 0.12
        lower_bound = price * (1 - mape)
        upper_bound = price * (1 + mape)

        st.subheader(f"Predicted Price: **${price:,.0f}**")
        st.markdown("#### Estimated Price Range")
        st.markdown(f"**Upper Range:** ${upper_bound:,.0f}")
        st.markdown(f"**Lower Range:** ${lower_bound:,.0f}")
        # SHAP explainer + plot
    try:
        explainer = shap.TreeExplainer(model)
    except Exception:
        masker = shap.maskers.Independent(input_df)  # background drawn from the row(s) you’re explaining
        predict_fn = getattr(model, "predict", None)
        if callable(predict_fn):
            explainer = shap.Explainer(predict_fn, masker)
        else:
            predict_proba = getattr(model, "predict_proba", None)
            if callable(predict_proba):
                explainer = shap.Explainer(lambda X: predict_proba(X)[:, 1], masker)
            else:
                st.error("Model has no predict/predict_proba; cannot build SHAP explainer.")
                st.stop()
    # Compute SHAP value
    shap_values = explainer(input_df)

    # Waterfall (single prediction)
    fig, ax = plt.subplots(figsize=(10, 4))
    shap.plots.waterfall(shap_values[0], show=False)
    st.pyplot(fig, clear_figure=True)

    # Save plot to buffer for download
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

        shap_values = explainer(input_df)
        fig, ax = plt.subplots(figsize=(10, 4))
        shap.plots.waterfall(shap_values[0], show=False)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.pyplot(fig)

        # Download SHAP plot
        st.download_button("Download SHAP Plot", data=buf.getvalue(), file_name="shap_plot.png", mime="image/png")

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Home Price Report", ln=True, align="C")
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Address: {full_address}", ln=True)
        pdf.cell(200, 10, txt=f"Predicted Price: ${price:,.0f}", ln=True)
        pdf.cell(200, 10, txt=f"Estimated Range: ${lower_bound:,.0f} - ${upper_bound:,.0f}", ln=True)

        # Add SHAP plot to PDF
        img_data = buf.getvalue()
        img_path = "temp_shap_plot.png"
        with open(img_path, "wb") as f:
            f.write(img_data)
        pdf.image(img_path, x=10, y=60, w=180)

        # Export PDF to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')

        # Download PDF
        st.download_button(
            "Download Full Report (PDF)",
            data=pdf_bytes,
            file_name="home_price_report.pdf",
            mime="application/pdf"
        )


with cols2:
    st.image("https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=800&q=80", use_container_width=True)
    
    

