import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Set Mapbox access token
px.set_mapbox_access_token("pk.eyJ1IjoiaW52ZXN0b3JzaG9yaXpvbiIsImEiOiJjbTk5Nm80NTUwYXJ0MnJxN3AyNWk2emgxIn0.vwAB8ce5FQpxMDxNLyrrMw")

# Load the socioeconomic data
df = pd.read_excel("Socioeconomic.xlsx", sheet_name=0)
df.columns = df.columns.str.strip()

# Load the GeoJSON file (must be in the same folder)
with open("nsw_suburbs.geojson") as f:
    geojson_data = json.load(f)

st.set_page_config(page_title="Socioeconomic Choropleth Map", layout="wide")
st.title("🗺️ Socioeconomic Choropleth Map")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# State filter
state_options = sorted(df["State"].dropna().unique())
selected_states = st.sidebar.multiselect("Select State(s):", options=state_options, default=state_options)

# Ranking range filter
min_rank = int(df["Socio-economic Ranking"].min())
max_rank = int(df["Socio-economic Ranking"].max())
selected_rank_range = st.sidebar.slider(
    "Select Socio-economic Ranking Range:",
    min_value=min_rank,
    max_value=max_rank,
    value=(min_rank, max_rank)
)

# Filtered data
filtered_df = df[
    (df["State"].isin(selected_states)) &
    (df["Socio-economic Ranking"] >= selected_rank_range[0]) &
    (df["Socio-economic Ranking"] <= selected_rank_range[1])
]

# Create the choropleth map
fig = px.choropleth_mapbox(
    filtered_df,
    geojson=geojson_data,
    locations="Suburb",  # must match GeoJSON field
    featureidkey="properties.Suburb",  # change this based on your GeoJSON structure
    color="Socio-economic Ranking",
    color_continuous_scale="YlGnBu",
    range_color=(min_rank, max_rank),
    mapbox_style="mapbox://styles/mapbox/streets-v12",
    zoom=6.5,
    center={"lat": -32.256943, "lon": 148.601105},  # centered on Dubbo
    opacity=0.6,
    height=750
)

st.plotly_chart(fig, use_container_width=True)
