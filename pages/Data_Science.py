import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import joblib
import matplotlib.pyplot as plt

model = joblib.load("pkl/xgb_home_price_model.pkl")
X_test = joblib.load("pkl/X_test.pkl")
y_test = joblib.load("pkl/y_test.pkl")
shap_values = joblib.load("pkl/shap_values.pkl")

preds = model.predict(X_test)


# Title and intro
st.title("Data Science Behind the App")
st.caption("For data scientists and technical experts: A deep dive into modeling, features, and interpretability.")

st.markdown("""
Welcome to the expert corner of **California Home Explorer**.  
Here you'll find an overview of the ML pipeline used to predict home prices — including model performance, feature engineering, and SHAP-based interpretation.
""")

# Section: Model Summary
st.header("Model Summary")
st.markdown("""
We evaluated **Linear Regression**, **Random Forest**, and **XGBoost**.  
**XGBoost** performed best with the following results:
- **R²**: 0.90  
- **RMSE**: ~$261,000  
- **MAPE**: ~12.2%
""")



# Section: Feature Engineering
st.header("Feature Engineering Highlights")
st.markdown("""
I engineered many powerful features:
- `LotPerLivingArea` – ratio of lot size to house size  
- `distance_to_downtown` – haversine distance to nearest major city  
- `Is_New`, `HasGarage`, `HasFireplace` – binary amenity flags  
- `LocationCluster` – region-based clusters from latitude & longitude  
""")



# Evaluation visual (Predicted vs Actual)
st.header("Predicted vs Actual Prices")
df_eval = pd.DataFrame({
    "Actual Price": y_test,
    "Predicted Price": preds
})

fig = px.scatter(df_eval, x="Actual Price", y="Predicted Price", trendline="ols")
fig.update_layout(title="Predicted vs Actual Prices", xaxis_tickprefix="$", yaxis_tickprefix="$")
st.plotly_chart(fig, use_container_width=True)

# SHAP explanation
st.header("SHAP Model Interpretability")
st.markdown("""
Using SHAP, I confirmed that features like `Longitude`, `Latitude`, and `LivingArea`  
had the greatest influence on predictions — aligning well with real estate intuition.
""")

import shap 

st.subheader("SHAP Summary Plot")
fig, ax = plt.subplots()
shap.plots.beeswarm(shap_values, max_display=15, show=False)
st.pyplot(fig)
