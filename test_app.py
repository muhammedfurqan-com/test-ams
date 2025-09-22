import streamlit as st
import requests
import matplotlib.pyplot as plt

API_KEY = "AIzaSyAhx1zMNWGZG2a45ZXm6o825Zzcjv-bUGk"

st.title("Wireless Link Path Profile Tool")

# User inputs
tx = st.text_input("TX coordinates (lat,lon)", "33.6844,73.0479")
rx = st.text_input("RX coordinates (lat,lon)", "32.0836,72.6711")
samples = st.slider("Number of samples along the path", 10, 500, 100)

if st.button("Fetch Elevation Data"):
    path = f"{tx}|{rx}"
    url = f"https://maps.googleapis.com/maps/api/elevation/json?path={path}&samples={samples}&key={API_KEY}"
    response = requests.get(url).json()

    if response.get("status") == "OK" and "results" in response:
        elevations = [p["elevation"] for p in response["results"]]

        min_elev = min(elevations)
        max_elev = max(elevations)
        start_elev = elevations[0]
        end_elev = elevations[-1]

        st.write(f"**Start point elevation (TX):** {start_elev:.1f} m")
        st.write(f"**End point elevation (RX):** {end_elev:.1f} m")
        st.write(f"**Minimum elevation along path:** {min_elev:.1f} m")
        st.write(f"**Maximum elevation along path:** {max_elev:.1f} m")
    else:
        st.error(f"Error: {response.get('error_message', response.get('status'))}")

if st.button("Generate Path Profile"):
    # Build API request
    path = f"{tx}|{rx}"
    url = f"https://maps.googleapis.com/maps/api/elevation/json?path={path}&samples={samples}&key={API_KEY}"
    response = requests.get(url).json()

    if response.get("status") == "OK" and "results" in response:
        elevations = [p["elevation"] for p in response["results"]]

        # Plot path profile
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(elevations, color="blue", linewidth=2, label="Terrain")
        ax.fill_between(range(len(elevations)), elevations, color="skyblue", alpha=0.3)
        ax.set_title("Elevation Path Profile (AMSL)", fontsize=14)
        ax.set_xlabel("Sample Points Along Path")
        ax.set_ylabel("Elevation (m)")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()

        st.pyplot(fig)

        # Show start & end elevations
        st.success(f"TX elevation: {elevations[0]:.1f} m, RX elevation: {elevations[-1]:.1f} m")
    else:
        st.error(f"Error fetching data: {response.get('error_message', response.get('status'))}")


st.title("Path Profile Checker")

#tx = st.text_input("TX coordinates (lat,lon)", "33.6844,73.0479")
#rx = st.text_input("RX coordinates (lat,lon)", "32.0836,72.6711")

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
