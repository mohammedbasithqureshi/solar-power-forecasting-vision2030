import streamlit as st
import pandas as pd
import joblib

model = joblib.load('models/solar_model.pkl')
model_columns = joblib.load('models/solar_model_columns.pkl')

st.title("☀️ Solar Power Output Predictor")
st.write("Predict solar plant AC power output based on time and environmental conditions.")

st.header("Input Conditions")

col1, col2 = st.columns(2)
with col1:
    hour = st.slider("Hour of Day", 0, 23, 12)
    ambient_temp = st.slider("Ambient Temperature (°C)", 15, 45, 28)
    module_temp = st.slider("Module Temperature (°C)", 15, 70, 45)
with col2:
    irradiation = st.slider("Irradiation (kW/m²)", 0.0, 1.3, 0.6, step=0.01)

is_daylight = 1 if 6 <= hour <= 18 else 0

# Recent output context (placeholder since we don't have live sensor feed)
ac_power_lag_1 = irradiation * 900  # rough proxy based on the strong linear relationship
ac_power_rolling_3 = ac_power_lag_1

input_dict = {
    'AMBIENT_TEMPERATURE': ambient_temp,
    'MODULE_TEMPERATURE': module_temp,
    'IRRADIATION': irradiation,
    'hour': hour,
    'is_daylight': is_daylight,
    'ac_power_lag_1': ac_power_lag_1,
    'ac_power_rolling_3': ac_power_rolling_3
}

input_df = pd.DataFrame([input_dict])[model_columns]

if st.button("Predict Power Output"):
    prediction = model.predict(input_df)[0]
    st.success(f"Predicted AC Power Output: **{prediction:.1f} kW**")

    st.bar_chart(pd.DataFrame({"Predicted Output (kW)": [prediction]}, index=["Prediction"]))

    # --- Vision 2030 / clean energy impact estimate (illustrative only) ---
    co2_per_kwh_avoided = 0.5  # kg CO2/kWh, rough grid-average displacement estimate
    hours_equivalent = 1  # treating this as a 1-hour output snapshot
    co2_avoided = (prediction * hours_equivalent / 1000) * co2_per_kwh_avoided * 1000  # kg

    st.info(
        f"🌍 At this output level, this generation could offset an estimated "
        f"**{co2_avoided:.1f} kg CO2/hour** compared to fossil-fuel grid power — "
        f"contributing to Saudi Arabia's Vision 2030 renewable energy targets. "
        f"*(Illustrative estimate only — not a validated emissions calculation.)*"
    )