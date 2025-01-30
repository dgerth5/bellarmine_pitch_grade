import streamlit as st
import pandas as pd
import numpy as np

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("asun_pitcher_summary.csv")

df = load_data()

# Compute percentiles and convert to 20-80 scale
def compute_grades(df, pitch_type, pitcher_throws, input_values):
    grades = {}
    filtered_df = df[(df["AutoPitchType"] == pitch_type) & (df["PitcherThrows"] == pitcher_throws)]
    
    for col in ["mean_velo", "mean_vmov", "mean_hmov", "mean_spin", "mean_vaa", "mean_ext"]:
        mean = filtered_df[col].mean()
        std = filtered_df[col].std()
        z_score = (input_values[col] - mean) / std
        grades[col] = 50 + (z_score * 10)  # Convert to 20-80 scale
        grades[col] = max(20, min(80, grades[col]))  # Ensure within scale range
    
    return grades

# Streamlit UI
st.title("Pitcher Performance Grade Finder")

st.sidebar.header("Input Your Pitch Values")

pitch_type = st.sidebar.selectbox("Select Pitch Type", df["AutoPitchType"].unique())
pitcher_throws = st.sidebar.selectbox("Pitcher Throws", ["Right", "Left"])
input_values = {}

for col in ["mean_velo", "mean_vmov", "mean_hmov", "mean_spin", "mean_vaa", "mean_ext"]:
    input_values[col] = st.sidebar.number_input(f"{col.replace('_', ' ').title()}", value=0.0)

if st.sidebar.button("Compute Grades"):
    result = compute_grades(df, pitch_type, pitcher_throws, input_values)
    
    st.subheader(f"Grades for {pitch_type} ({pitcher_throws}-handed)")
    for metric, grade in result.items():
        st.write(f"{metric.replace('_', ' ').title()}: {int(round(grade))} grade")
