import streamlit as st
import folium
from streamlit_folium import st_folium
import random
from streamlit_autorefresh import st_autorefresh

# Simulated robot data fetch
def fetch_robot_data():
    return [
        {
            "id": "R1", "lat": random.uniform(37.7749, 37.7769), "lng": random.uniform(-122.4194, -122.4174),
            "status": random.choice(["Active", "Idle", "Charging"]),
            "battery": random.randint(50, 100),
            "soil_moisture": random.uniform(10, 100),
            "temperature": random.uniform(15, 35),
            "crop_health": random.choice(["Healthy", "Needs Attention", "Critical"])
        },
        {
            "id": "R2", "lat": random.uniform(37.7749, 37.7769), "lng": random.uniform(-122.4194, -122.4174),
            "status": random.choice(["Active", "Idle", "Charging"]),
            "battery": random.randint(50, 100),
            "soil_moisture": random.uniform(10, 100),
            "temperature": random.uniform(15, 35),
            "crop_health": random.choice(["Healthy", "Needs Attention", "Critical"])
        },
    ]

# Streamlit UI
def fleet_dashboard():
    st.set_page_config(page_title="SLAMBot Fleet Dashboard", layout="wide")
    st.title("🚜 SLAMBot Fleet Dashboard (Smart Agriculture)")

    # Auto-refresh every 5 seconds
    st_autorefresh(interval=5000, key="fleet_refresh")

    # Initialize session state if not already present
    if "robots" not in st.session_state:
        st.session_state.robots = fetch_robot_data()

    # Fleet Map
    st.subheader("🌍 Fleet Map")
    fleet_map = folium.Map(location=[37.775, -122.418], zoom_start=15)

    # Add robot markers to the map
    for bot in st.session_state.robots:
        folium.Marker(
            location=[bot["lat"], bot["lng"]],
            popup=(
                f"<strong>{bot['id']}</strong><br>"
                f"Status: {bot['status']}<br>"
                f"🔋 Battery: {bot['battery']}%<br>"
                f"🌱 Soil Moisture: {bot['soil_moisture']}%<br>"
                f"🌡 Temperature: {bot['temperature']}°C<br>"
                f"🚜 Crop Health: {bot['crop_health']}"
            ),
            icon=folium.Icon(color="green" if bot["status"] == "Active" else "blue"),
        ).add_to(fleet_map)

    # Display the map in Streamlit
    st_folium(fleet_map, width=700, height=500)

    # Robot Status Panel
    st.subheader("📊 Robot Status")
    for bot in st.session_state.robots:
        st.markdown(
            f"{bot['id']}** - {bot['status']} | 🔋 {bot['battery']}% | "
            f"🌱 {bot['soil_moisture']}% | 🌡 {bot['temperature']}°C | 🚜 {bot['crop_health']}"
        )

    # Fleet Controls (Start and Stop)
    st.subheader("🎛 Fleet Controls")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Fleet", key="start_fleet"):
            st.session_state.fleet_status = "started"
            st.success("Fleet started! Robots navigating...")

    with col2:
        if st.button("Stop Fleet", key="stop_fleet"):
            st.session_state.fleet_status = "stopped"
            st.warning("Fleet stopped! All robots are idle.")

# Run Streamlit App
if _name_ == "_main_":
    fleet_dashboard()
