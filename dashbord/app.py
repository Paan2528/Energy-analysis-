import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8002"

st.title("Solar Energy Dashboard (project 3)")

# Metics
metrics = requests.get(f"{API}/energy/metrics").json()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Days", metrics.get("day", 0))
c2.metric("Avg Energy (MW)", f"{metrics.get('avg_energy', 0)/1000:,.2f}")
c3.metric("Max Energy (MW)", f"{metrics.get('max_energy', 0)/1000:,.2f}")
c4.metric("Anomaly%", f"{metrics.get('anomaly_pct', 0):,.1f}%")

# Daily Data
daily = requests.get(f"{API}/energy/daily").json()
df = pd.DataFrame(daily)

if df.empty:
    st.warning("No data returned from API.")
    st.stop()

df["day"] = pd.to_datetime(df["day"])
df = df.sort_values("day")

# Data Filter
st.subheader("Filter by data")
start = st.date_input("Start date", df["day"].min().date())
end = st.date_input("End date", df["day"].max().date())

df_f = df[(df["day"].dt.date >= start) & (df["day"].dt.date <= end)]

# Chart
st.subheader("Daily Energy(Line Chart)")
st.line_chart(df_f.set_index("day")["energy"])

# Highlight anomalies(table + count)
st.subheader("Anomalies in selected range")
anoms = df_f[df_f["is_anomaly"] == True]
st.write(f"Anomaly count: **{len(anoms)}**")
st.dataframe(anoms, use_container_width=True)

# full table(optional)
with st.expander("Show raw date"):
    st.dataframe(df_f, use_container_width=True)
