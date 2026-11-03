
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
    background-color: #0b1120;
    color: #f1f5f9;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(120deg, #172554, #164e63);
    margin-bottom: 25px;
    border: 1px solid #334155;
}

.hero h1 {
    color: white;
    font-size: 35px;
    margin-bottom: 8px;
}

.hero p {
    color: #cbd5e1;
    font-size: 16px;
}

.section-card {
    background-color: #151f32;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #334155;
    margin-bottom: 20px;
}

.location-card {
    background-color: #123b35;
    border: 1px solid #16a34a;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
}

div[data-testid="stMetric"] {
    background-color: #151f32;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #334155;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 9px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
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
# MODE SELECTION
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

# ==================================================
# DEMO MODE
# ==================================================

if mode == "Demo Mode":

    st.info(
        "Demo Mode: Select a saved Wi-Fi fingerprint "
        "to simulate AI location prediction."
    )

    sample_index = st.selectbox(
        "Select a Wi-Fi fingerprint",
        range(len(df)),
        format_func=lambda x: f"Sample {x + 1}",
        key="demo_sample"
    )

    sample = df.iloc[sample_index]

    scan_readings = sample.drop(
        ["scan_key", "location_id", "location_name", "floor"]
    ).to_dict()

    try:

        predicted_location, confidence = predict_location(
            scan_readings
        )

    except Exception as error:

        st.error(f"Prediction failed: {error}")
        st.stop()

    st.markdown(
        f"""
        <div class="location-card">
            <h4>📍 Predicted Current Location</h4>
            <h3>{predicted_location}</h3>
            <p>Demo prediction using saved Wi-Fi fingerprint</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "AI Prediction Confidence",
            f"{confidence:.2f}%"
        )

    with col2:

        st.metric(
            "Available Fingerprints",
            len(df)
        )

# ==================================================
# LIVE WI-FI MODE
# ==================================================

else:

    st.info(
        "Live Mode: Use your Motorola Android application "
        "to scan nearby Wi-Fi access points and send the scan "
        "to the Flask API."
    )

    st.markdown("### 📡 Live Wi-Fi Connection")

    st.write(
        "1. Open the Android Indoor Navigation application."
    )

    st.write(
        "2. Scan Wi-Fi networks and send the scan."
    )

    st.write(
        "3. Click the button below to retrieve the latest prediction."
    )

    if st.button(
        "🔄 Refresh Latest Wi-Fi Location",
        use_container_width=True
    ):

        st.session_state.pop("live_location_data", None)

        result, error = get_live_location()

        if result:

            st.session_state["live_location_data"] = result

        else:

            st.session_state["live_location_error"] = error

    # Display previously retrieved live location

    if "live_location_data" in st.session_state:

        live_data = st.session_state["live_location_data"]

        predicted_location = live_data.get(
            "current_location"
        )

        confidence = live_data.get(
            "confidence"
        )

        matched_access_points = live_data.get(
            "matched_access_points"
        )

        st.markdown(
            f"""
            <div class="location-card">
                <h4>📍 Live Predicted Current Location</h4>
                <h3>{predicted_location}</h3>
                <p>Location predicted from Android Wi-Fi scan</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "AI Confidence",
                f"{confidence:.2f}%"
            )

        with col2:

            st.metric(
                "Matched Access Points",
                matched_access_points
            )

        with col3:

            st.metric(
                "Model Features",
                live_data.get("total_model_features", 48)
            )

        st.caption(
            "Last scan: " +
            str(live_data.get("last_updated", "Unknown"))
        )

        st.success(
            "Live location retrieved successfully!"
        )

    else:

        st.warning(
            st.session_state.get(
                "live_location_error",
                "Waiting for the first Android Wi-Fi scan. "
                "Send a scan from your phone and refresh this page."
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

st.subheader("🎯 Where Would You Like to Go?")

destination = st.selectbox(
    "Choose your destination",
    locations
)

# ==================================================
# SHORTEST ROUTE
# ==================================================

if st.button(
    "🧭 Find My Shortest Route",
    use_container_width=True
):

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
                    "Current Position"
                )

                st.caption(start)

            with col2:

                st.metric(
                    "Destination",
                    "Selected Location"
                )

                st.caption(destination)

            with col3:

                st.metric(
                    "Approximate Distance",
                    f"{distance} m"
                )

            st.divider()

            # ------------------------------------------
            # ROUTE OVERVIEW
            # ------------------------------------------

            st.subheader("🗺️ Route Overview")

            for i, location in enumerate(
                route,
                start=1
            ):

                if i == 1:

                    st.markdown(
                        f"🟢 **START:** {location}"
                    )

                elif i == len(route):

                    st.markdown(
                        f"🔴 **DESTINATION:** {location}"
                    )

                else:

                    st.markdown(
                        f"⬇️ {location}"
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
            # WALKING DIRECTIONS
            # ------------------------------------------

            st.subheader(
                "🚶 Step-by-Step Walking Directions"
            )

            instructions = generate_instructions(route)

            for i, instruction in enumerate(
                instructions,
                start=1
            ):

                st.markdown(
                    f"""
                    <div class="section-card">
                        <h4>Step {i}</h4>
                        <p>{instruction}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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