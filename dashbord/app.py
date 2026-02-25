import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8002"

st.title("Solar Energy Dashboard (project 4)")

# Metics
metrics = requests.get(f"{API}/energy/metrics").json()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Days", metrics.get("day", 0))
c2.metric("Avg Energy (MW)", f"{metrics.get('avg_energy', 0)/1000:,.2f}")
c3.metric("Max Energy (MW)", f"{metrics.get('max_energy', 0)/1000:,.2f}")
c4.metric("Anomaly%", f"{metrics.get('anomaly_pct', 0):,.1f}%")

# Project4
st.subheader("Filter by date")
all_daily = requests.get(f"{API}/energy/daily").json()
df_all = pd.DataFrame(all_daily)
df_all["day"] = pd.to_datetime(df_all["day"])
min_day = df_all["day"].min().date()
max_day = df_all["day"].max().date()

start = st.date_input("Start", min_day)
end = st.date_input("End", max_day)


# Daily Data
daily = requests.get(f"{API}/energy/daily", params={"start": start, "end": end}).json()
df = pd.DataFrame(daily)
df["day"] = pd.to_datetime(df["day"])
df = df.sort_values("day")

df["energy_mw"] = df["energy"] / 1000

st.subheader("Daily Energy (MW)")
st.line_chart(df.set_index("day")["energy_mw"])

anoms = df[df["is_anomaly"] == True]
st.subheader("Anomalies")
st.write(f"Count: {len(anoms)}")
st.dataframe(anoms, use_container_width=True)
