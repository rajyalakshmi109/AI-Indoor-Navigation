
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import json
import urllib.request
import urllib.error

from pathlib import Path
from directions import generate_instructions
from navigation import find_shortest_route
from location_prediction import predict_location
from maps.route_visualization import draw_ground_floor, draw_first_floor

# ==================================================
# PROJECT CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="AI Indoor Navigation",
    page_icon="📍",
    layout="wide"
)

API_URL = "http://127.0.0.1:5000"

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
    color: #24344D;
}
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1380px;
}
.hero {
    padding: 26px 30px;
    border-radius: 14px;
    background: #FFFFFF;
    margin-bottom: 24px;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #4776A8;
    box-shadow: 0 2px 8px rgba(30, 55, 90, 0.04);
}
.hero h1 {
    color: #243B5A;
    font-size: 31px;
    font-weight: 700;
    margin: 0 0 7px 0;
}
.hero p {
    color: #64748B;
    font-size: 15px;
    margin: 0;
}
.section-card, .location-card {
    background: #FFFFFF;
    padding: 20px 22px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(30, 55, 90, 0.035);
}
.location-card {
    border-left: 4px solid #4776A8;
}
.location-card h4 {
    color: #64748B;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
}
.location-card h3 {
    color: #243B5A;
    font-size: 23px;
    margin: 0 0 6px 0;
}
.location-card p {
    color: #64748B;
    margin: 0;
}
div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 16px 18px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(30, 55, 90, 0.035);
}
div[data-testid="stMetricLabel"] {
    color: #64748B;
}
div[data-testid="stMetricValue"] {
    color: #243B5A;
    font-size: 1.35rem;
    line-height: 1.35;
    overflow-wrap: anywhere;
}
div[data-baseweb="select"] * {
    color: #243B5A !important;
}
div.stButton > button {
    background: #4776A8;
    color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #4776A8;
    padding: 9px 20px;
    font-weight: 600;
    min-height: 42px;
}
div.stButton > button:hover {
    background: #365F8B;
    border-color: #365F8B;
    color: #FFFFFF;
}
div[data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-color: #CBD5E1;
    border-radius: 8px;
}
div[role="radiogroup"] {
    gap: 16px;
}
h1, h2, h3, h4 {
    color: #243B5A;
}
p, label, .stMarkdown {
    color: #475569;
}
button[data-baseweb="tab"] {
    color: #475569;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #365F8B;
    border-bottom-color: #4776A8;
}
hr {
    border-color: #DCE4EE;
}
div[data-testid="stAlert"] {
    border-radius: 10px;
}
/* Section headings and balanced two-column panels */
.section-heading {
    color: #243B5A;
    font-size: 1.12rem;
    font-weight: 700;
    margin: 4px 0 12px 0;
}
.panel {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px 20px;
    min-height: 100%;
    box-shadow: 0 2px 8px rgba(30, 55, 90, 0.035);
}
.panel-label {
    color: #64748B;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
}
.route-item {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 11px 14px;
    margin: 8px 0;
    color: #334155;
}
.route-step {
    color: #4776A8;
    font-weight: 700;
    margin-right: 8px;
}
div[data-testid="stVerticalBlock"] > div:has(> div > .panel) {
    height: 100%;
}
@media (max-width: 800px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <h1>🏢 AI Indoor Navigation</h1>
    <p>
        Intelligent indoor positioning and shortest-path navigation
        using Wi-Fi Fingerprinting and Machine Learning.
    </p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# DESTINATIONS
# ==================================================

locations = [
    "Ground Floor Library Entrance",
    "Ground Floor Study Hall 2 Entrance",
    "Ground Floor Library Hall 2 Entrance",
    "Ground Floor Staircase Entrance",
    "Ground Floor Study Hall Centre",
    "Ground Floor Library Hall 2 Centre",
    "First Floor Staircase Landing",
    "First Floor Computer Centre Entrance",
    "First Floor Computer Lab 2",
    "First Floor Ojah Ma'am's Cabin"
]

# ==================================================
# API FUNCTION
# ==================================================

def get_live_location():

    url = API_URL + "/live-location"

    try:

        request = urllib.request.Request(
            url,
            headers={"Accept": "application/json"}
        )

        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

            return result, None

    except urllib.error.HTTPError as error:

        try:
            message = json.loads(
                error.read().decode("utf-8")
            )
        except Exception:
            message = {"message": str(error)}

        return None, message.get("message", str(error))

    except Exception as error:

        return None, str(error)

# ==================================================
# LOAD DEMO DATASET
# ==================================================

dataset_path = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "scan_fingerprints.csv"
)

if not dataset_path.exists():

    st.error("Wi-Fi fingerprint dataset was not found.")
    st.stop()

df = pd.read_csv(dataset_path)

if df.empty:

    st.error("The Wi-Fi fingerprint dataset is empty.")
    st.stop()

# ==================================================
# MODE SELECTION AND LOCATION DETECTION
# ==================================================

st.subheader("🤖 AI Location Detection")

mode = st.radio(
    "Select Navigation Mode",
    ["Demo Mode", "Live Wi-Fi Mode"],
    horizontal=True
)

predicted_location = None
confidence = None
matched_access_points = None

if mode == "Demo Mode":

    left_col, right_col = st.columns([1, 1.25], gap="large")

    with left_col:
        st.markdown('<div class="panel-label">Demo controls</div>', unsafe_allow_html=True)
        st.info(
            "This mode uses Wi-Fi fingerprints collected earlier in the building. "
            "Each fingerprint contains recorded BSSID and RSSI values. "
            "The Random Forest model predicts the location from those readings."
        )

        st.markdown("**Saved Wi-Fi fingerprint records**")

        def fingerprint_label(index):
            row = df.iloc[index]
            actual_location = str(row.get("location_name", "Unknown location"))
            floor_name = str(row.get("floor", "")).strip()
            floor_text = f" | {floor_name}" if floor_name and floor_name.lower() != "nan" else ""
            return f"Fingerprint {index + 1} — {actual_location}{floor_text}"

        sample_index = st.selectbox(
            "Select a collected fingerprint",
            range(len(df)),
            format_func=fingerprint_label,
            key="demo_sample"
        )

        sample = df.iloc[sample_index]
        scan_readings = sample.drop(
            ["scan_key", "location_id", "location_name", "floor"]
        ).to_dict()

        try:
            predicted_location, confidence = predict_location(scan_readings)
        except Exception as error:
            st.error(f"Prediction failed: {error}")
            st.stop()

        st.caption("The selected record is a previously collected Wi-Fi scan. The model prediction is shown separately for comparison with its recorded location.")

    with right_col:
        st.markdown('<div class="panel-label">Detected location</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="location-card">
                <h4>📍 Predicted Current Location</h4>
                <h3>{predicted_location}</h3>
                <p>AI prediction using the saved Wi-Fi fingerprint</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        metric_a, metric_b = st.columns(2)
        with metric_a:
            st.metric("AI Confidence", f"{confidence:.2f}%")
        with metric_b:
            st.metric("Available Fingerprints", len(df))

else:

    left_col, right_col = st.columns([1, 1.25], gap="large")

    with left_col:
        st.markdown('<div class="panel-label">Connect your Android device</div>', unsafe_allow_html=True)
        st.info(
            "Use the Android application to scan nearby Wi-Fi access points. "
            "The scan is sent to the Flask API running on this laptop."
        )
        st.markdown("**How to update your position**")
        st.write("1. Open the Android Indoor Navigation app.")
        st.write("2. Scan nearby Wi-Fi networks and send the scan.")
        st.write("3. Refresh the latest location here.")

        if st.button("🔄 Refresh Latest Wi-Fi Location", use_container_width=True):
            st.session_state.pop("live_location_data", None)
            result, error = get_live_location()
            if result:
                st.session_state["live_location_data"] = result
                st.session_state.pop("live_location_error", None)
            else:
                st.session_state["live_location_error"] = error

    with right_col:
        st.markdown('<div class="panel-label">Live positioning result</div>', unsafe_allow_html=True)

        if "live_location_data" in st.session_state:
            live_data = st.session_state["live_location_data"]
            predicted_location = live_data.get("current_location")
            confidence = live_data.get("confidence")
            matched_access_points = live_data.get("matched_access_points")

            st.markdown(
                f"""
                <div class="location-card">
                    <h4>📍 Live Predicted Current Location</h4>
                    <h3>{predicted_location}</h3>
                    <p>Location predicted from the latest Android Wi-Fi scan</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            metric_a, metric_b, metric_c = st.columns(3)
            with metric_a:
                st.metric("AI Confidence", f"{confidence:.2f}%")
            with metric_b:
                st.metric("Matched APs", matched_access_points)
            with metric_c:
                st.metric("Model Features", live_data.get("total_model_features", 48))
            st.caption("Last scan: " + str(live_data.get("last_updated", "Unknown")))
        else:
            st.warning(
                st.session_state.get(
                    "live_location_error",
                    "Waiting for the first Android Wi-Fi scan. Send a scan and refresh this panel."
                )
            )

# ==================================================
# STOP IF LOCATION IS NOT AVAILABLE
# ==================================================

if predicted_location is None:

    st.divider()

    st.caption(
        "A valid location prediction is required before "
        "shortest-path navigation can begin."
    )

    st.stop()

# ==================================================
# DESTINATION SELECTION
# ==================================================

st.divider()

st.subheader("🎯 Plan Your Destination")

destination_col, action_col = st.columns([2, 1], gap="large")
with destination_col:
    destination = st.selectbox(
        "Choose your destination",
        locations
    )
with action_col:
    find_route_clicked = st.button(
        "🧭 Find My Shortest Route",
        use_container_width=True
    )

# ==================================================
# SHORTEST ROUTE
# ==================================================

if find_route_clicked:

    start = str(predicted_location)

    if start == destination:

        st.success(
            "🎉 You are already at your destination!"
        )

    else:

        route, distance = find_shortest_route(
            start,
            destination
        )

        if route:

            st.success(
                "✅ Shortest route calculated successfully!"
            )

            # ------------------------------------------
            # JOURNEY SUMMARY
            # ------------------------------------------

            st.subheader("📌 Your Journey")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Starting Location",
                    start
                )

            with col2:

                st.metric(
                    "Destination",
                    destination
                )

            with col3:

                st.metric(
                    "Approximate Distance",
                    f"{distance} m"
                )

            st.divider()

            # ------------------------------------------
            # ROUTE OVERVIEW
            # ------------------------------------------

            route_col, directions_col = st.columns([1, 1.25], gap="large")

            with route_col:
                st.subheader("🗺️ Route Overview")
                for i, location in enumerate(route, start=1):
                    if i == 1:
                        label = "🟢 START"
                    elif i == len(route):
                        label = "🔴 DESTINATION"
                    else:
                        label = "📍 WAYPOINT"
                    st.markdown(
                        f'<div class="route-item"><span class="route-step">{label}</span><br>{location}</div>',
                        unsafe_allow_html=True
                    )

            with directions_col:
                st.subheader("🚶 Step-by-Step Directions")
                instructions = generate_instructions(route)
                for i, instruction in enumerate(instructions, start=1):
                    st.markdown(
                        f"""
                        <div class="section-card">
                            <h4>Step {i}</h4>
                            <p>{instruction}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.divider()

            # ------------------------------------------
            # FLOOR MAPS
            # ------------------------------------------

            st.subheader(
                "🏢 Interactive Floor Map View"
            )

            ground_locations = [
                location for location in route
                if location.startswith("Ground Floor")
            ]

            first_locations = [
                location for location in route
                if location.startswith("First Floor")
            ]

            tabs = st.tabs([
                "Ground Floor",
                "First Floor"
            ])

            with tabs[0]:

                if ground_locations:

                    st.caption(
                        "Ground Floor schematic showing "
                        "the selected route."
                    )

                    ground_fig = draw_ground_floor(route)

                    st.pyplot(
                        ground_fig,
                        use_container_width=True
                    )

                    plt.close(ground_fig)

                else:

                    st.info(
                        "Your route does not pass through "
                        "the Ground Floor."
                    )

            with tabs[1]:

                if first_locations:

                    st.caption(
                        "First Floor schematic showing "
                        "the selected route."
                    )

                    first_fig = draw_first_floor(route)

                    st.pyplot(
                        first_fig,
                        use_container_width=True
                    )

                    plt.close(first_fig)

                else:

                    st.info(
                        "Your route does not pass through "
                        "the First Floor."
                    )

            st.divider()

            # ------------------------------------------
            # FINAL MESSAGE
            # ------------------------------------------

            st.success(
                "🎉 Your navigation route is ready! "
                "Follow the walking directions to reach "
                "your destination."
            )

            st.caption(
                "Distances are approximate. Maps are "
                "schematic representations of the building."
            )

        else:

            st.error(
                "No route is available between these locations."
            )

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "AI-Based Indoor Navigation System | "
    "Wi-Fi Fingerprinting • Random Forest • Dijkstra Algorithm"
)