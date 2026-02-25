import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8002"

st.title("Solar Energy Dashboard (project 3)")

# load data from API
resp = requests.get(f"{API}/energy/daily")
data = resp.json()

df = pd.DataFrame(data)

if df.empty:
    st.write("No data returned from API. Check DB + populate script.")
    st.stop()
df["day"] = pd.to_datetime(df["day"])
df = df.sort_values("day")

# Show table
st.subheader("Daily Energy Data")
st.dataframe(df, use_container_width=True)

# Liine chart
st.subheader("Daily Energy Line Chart")
st.line_chart(df.set_index("day")["energy"])

# Anomalies
st.subheader("Anomaly Days")
anoms = df[df["is_anomaly"] == True]
st.write(f"Anomaly count: {len(anoms)}")
st.dataframe(anoms, use_container_width=True)
