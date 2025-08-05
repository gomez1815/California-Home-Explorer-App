import streamlit as st

st.title("Data Sources")

st.markdown("""
### Overview of Data Sources Used

- **Housing data**  
  Downloaded via secure FTP from `ftp.boxgrad.com` using FileZilla.  
  I used the most recent 6 months of **CRMLS residential single-family** property sales, located in the `/raw/California` directory.

- **Metadata**  
  Variable definitions and dataset structure were referenced from  
  `Trestle Property MetaData.pdf` in the `/resources` folder on the FTP server.

- **Geolocation**  
  I use the [Nominatim API](https://nominatim.openstreetmap.org/) to retrieve location metadata (such as city, zip code) from latitude and longitude.

- **Distance to Coastline**  
  Calculated as the geodesic (straight-line) distance from each property to the **nearest of 10 key California coastal cities**:  
  Crescent City, Eureka, Mendocino, San Francisco, Santa Cruz, Monterey,  
  Pismo Beach, Santa Barbara, Santa Monica, and San Diego.

- **Distance to Major City Centers**  
  Calculated as the distance to the **nearest of 6 major urban hubs**:  
  Los Angeles, San Francisco, San Diego, Sacramento, San Jose, and Fresno.

- **City Rankings**  
  Rankings were constructed using actual transaction data:  
  - **Expensive Cities**: Top 100 cities by **mean home sale price**.  
  - **Cheap Cities**: Top 100 cities with the **lowest mean home sale price**.  
  - **Famous Cities**: Cities with the **highest number of transactions** in the dataset.  
""")
