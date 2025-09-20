import streamlit as st
import requests
import matplotlib.pyplot as plt

API_KEY = "YOUR_API_KEY"

st.title("Path Profile Checker")

tx = st.text_input("TX coordinates (lat,lon)", "33.6844,73.0479")
rx = st.text_input("RX coordinates (lat,lon)", "32.0836,72.6711")

if st.button("Check Path Profile"):
    path = f"{tx}|{rx}"
    url = f"https://maps.googleapis.com/maps/api/elevation/json?path={path}&samples=50&key={API_KEY}"
    response = requests.get(url).json()
    st.write(response)


    profile = [p["elevation"] for p in response["results"]]

    # Create figure
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(profile, color="blue", linewidth=2)   # Blue line
    ax.fill_between(range(len(profile)), profile, color="skyblue", alpha=0.3)  # Fill under curve

    ax.set_title("Elevation Profile", fontsize=14)
    ax.set_xlabel("Sample Point")
    ax.set_ylabel("Elevation (m AMSL)")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)
