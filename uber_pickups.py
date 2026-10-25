import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")
st.caption("Streamlit tutorial · September 2014 pickup data · first 10,000 rows")

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.columns = data.columns.str.lower()
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

with st.spinner("Loading pickup data..."):
    data = load_data(10000)

st.write(f"Loaded {len(data):,} pickups.")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

st.subheader("Number of pickups by hour")
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24)
)[0]

hourly = pd.DataFrame({
    "Hour": np.arange(24),
    "Pickups": hist_values,
})
st.bar_chart(hourly.set_index("Hour"))

hour_to_filter = st.slider("Hour", 0, 23, 17)
filtered_data = data[
    data[DATE_COLUMN].dt.hour == hour_to_filter
]

st.subheader(f"Map of pickups from {hour_to_filter:02d}:00–{hour_to_filter:02d}:59")
st.write(f"{len(filtered_data):,} pickups in this hour.")
st.map(filtered_data)
