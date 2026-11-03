# AI-Based Indoor Navigation Using Wi-Fi Fingerprinting

> An academic prototype for indoor localization and shortest-path
> navigation in a two-floor college building using Wi-Fi fingerprints,
> machine learning and graph algorithms.

## Project at a glance

  Item                     Details
  ------------------------ -------------------------------------------
  Localization approach    Wi-Fi fingerprinting using BSSID and RSSI
  Machine-learning model   Random Forest classifier
  Navigation algorithm     Dijkstra's shortest path
  Mobile client            Android application (Kotlin)
  Backend                  Flask REST API
  Dashboard                Streamlit
  Mapped environment       10 reference locations across 2 floors
  Fingerprint features     48 BSSID features
  Collected dataset        102 labelled fingerprints

## Live demo and repository

-   **Live Streamlit dashboard:**
    https://ai-indoor-navigation-axpyw4ffwhpq2zjte3acax.streamlit.app
-   **Flask API health check:**
    https://ai-indoor-navigation.onrender.com/health
-   **Source code:**
    https://github.com/rajyalakshmi109/AI-Indoor-Navigation

The dashboard provides a Demo Mode. Live Wi-Fi operation requires scans
from the mapped college-building environment. The free backend service
may take some time to wake after inactivity.

## 1. Problem statement

GPS signals can be weakened or blocked by roofs and walls, making
reliable room-level positioning difficult indoors. This project explores
Wi-Fi fingerprinting as an alternative way to estimate a user's location
within a mapped building and guide them to a selected destination.

## 2. Project objectives

1.  Collect labelled Wi-Fi fingerprints at known indoor locations.
2.  Preprocess and align Wi-Fi scan data into a consistent feature set.
3.  Train and evaluate a machine-learning model for indoor location
    classification.
4.  Integrate Android Wi-Fi scanning with a Flask backend.
5.  Calculate a minimum-cost route to a selected destination.
6.  Display the predicted location, route map and walking instructions.

## 3. System architecture and workflow

``` text
Android application
       |
       | Wi-Fi scan: BSSID + RSSI
       v
Flask REST API
       |
       | Validate readings and align 48 features
       v
Random Forest localization model
       |
       | Predicted indoor location
       v
Dijkstra route planning
       |
       | Route, approximate distance, instructions
       v
Streamlit dashboard / Android result screen
```

### End-to-end workflow

1.  The Android application scans nearby Wi-Fi access points and
    collects BSSID/RSSI readings.
2.  The app sends the readings and selected destination to the Flask
    `/navigate` endpoint.
3.  The backend aligns observed BSSIDs to the model's fixed 48-feature
    order. Missing trained access points are represented as `-100 dBm`.
4.  The Random Forest model predicts one of the labelled indoor
    locations and returns a confidence estimate.
5.  The navigation module uses Dijkstra's algorithm on the indoor
    connectivity graph to calculate a minimum-cost route.
6.  The API returns the predicted location, destination, route,
    approximate distance and walking instructions.
7.  The Streamlit dashboard displays the prediction, floor map,
    highlighted route and instructions.

## 4. Dataset and preprocessing

The collected dataset contains **102 labelled Wi-Fi fingerprints** from
**10 reference locations** across **two floors**.

A fingerprint represents one Wi-Fi scan captured at a known location.

-   **BSSID:** identifies a Wi-Fi access point.
-   **RSSI:** represents received signal strength, measured in dBm.
-   **Feature alignment:** every scan is represented using the same 48
    BSSID feature columns.
-   **Missing access points:** represented as `-100 dBm`.
-   **Target label:** the known location where the scan was collected.

### Session-based train/test split

  Collection sessions   Use                  Fingerprints
  --------------------- ------------------ --------------
  Sessions 1--2         Training                       82
  Sessions 3--4         Held-out testing               20
  **Total**                                       **102**

The test sessions were collected separately from the training sessions
to evaluate the model on later collection sessions rather than randomly
mixing scans.

> **Dataset limitation:** 102 fingerprints is a small dataset for 10
> locations. The held-out test set contains only two samples per
> location, so individual errors can substantially affect per-location
> metrics.

## 5. Localization model

A **Random Forest classifier** maps the aligned RSSI fingerprint to one
of the labelled indoor locations. It is the model used in the live
localization pipeline.

### Why Random Forest?

-   Uses an ensemble of decision trees.
-   Can model non-linear relationships between Wi-Fi signal features.
-   Works with structured, tabular feature data.
-   Provides class-probability estimates that can support a
    confidence-aware interface.

An Artificial Neural Network (ANN) was explored separately; it was not
the live model used for the reported test.

## 6. Route planning with Dijkstra's algorithm

The mapped building is represented as a graph:

-   **Nodes** represent mapped indoor locations.
-   **Edges** represent walkable connections.
-   **Edge weights** represent approximate travel distance or cost.
-   **Floor transitions** are represented explicitly as graph
    connections.

Dijkstra's algorithm finds a minimum-cost path from the predicted
current location to the selected destination.

**Example route observed in the project:**

``` text
Ground Floor Study Hall Centre
        |
        v
Ground Floor Study Hall 2 Entrance
        |
        v
Ground Floor Library Entrance
```

The example route was approximately **9 m** according to the graph. This
is an approximate schematic graph distance, not a surveyed
physical-distance guarantee.

## 7. Technology stack

  -----------------------------------------------------------------------
  Component               Technology              Purpose
  ----------------------- ----------------------- -----------------------
  Mobile application      Kotlin / Android        Wi-Fi scanning and
                                                  destination selection

  Backend API             Python / Flask          Receive scans and
                                                  return
                                                  predictions/routes

  Localization            Scikit-learn / Random   Predict indoor location
                          Forest                  

  Data processing         Pandas / NumPy          Clean and transform
                                                  fingerprints

  Route planning          NetworkX / Dijkstra     Compute minimum-cost
                                                  route

  Dashboard               Streamlit               Display prediction,
                                                  maps and directions

  Visualization           Matplotlib              Draw floor maps and
                                                  highlighted routes

  Deployment              Render / Streamlit      Host backend and
                          Community Cloud         dashboard
  -----------------------------------------------------------------------

## 8. Evaluation results

### Offline session-based model evaluation

  Metric                   Result
  --------------------- ---------
  Correct predictions     16 / 20
  Accuracy                **80%**
  Macro precision             70%
  Macro recall                80%
  Macro F1-score           73.33%

The Random Forest model was trained on 82 fingerprints from Sessions
1--2 and evaluated on 20 held-out fingerprints from Sessions 3--4.

### Live location checks

During the reported live college-building checks, **9 of 10** tested
locations were predicted correctly. One location was misclassified.

This is an observed demonstration result, not a statistically
established 90% building-wide accuracy. It should be considered
separately from the offline session-based test.

### Interpretation

Some live scans matched only 1--3 of the 48 trained BSSIDs. Low feature
overlap can make predictions less reliable, particularly when the scan
is taken outside the mapped building or in a different radio
environment.

## 9. API endpoints

  HTTP method   Endpoint           Purpose
  ------------- ------------------ ----------------------------------------
  `GET`         `/health`          Check whether the API is running
  `GET`         `/destinations`    Retrieve selectable destinations
  `POST`        `/predict`         Predict a location from Wi-Fi readings
  `GET`         `/live-location`   Retrieve the latest live prediction
  `POST`        `/navigate`        Predict location and calculate a route

The Android application sends a JSON request containing `scan_readings`
and `destination` to the `/navigate` endpoint.

## 10. Run the project locally

### Prerequisites

-   Python installed
-   Git
-   Android Studio (if building/running the Android client)
-   A compatible Android phone with Wi-Fi and required permissions for
    live scanning

### Step 1: Clone the repository

``` bash
git clone https://github.com/rajyalakshmi109/AI-Indoor-Navigation.git
cd AI-Indoor-Navigation
```

### Step 2: Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Python dependencies

``` bash
pip install -r requirements.txt
```

### Step 4: Start the Flask backend

``` bash
python api.py
```

The development server runs on port `5000` when started using the
project's local entry point.

### Step 5: Start the Streamlit dashboard

Open a second terminal, activate the same virtual environment, and run:

``` bash
streamlit run app.py
```

For local live-mode testing, set the dashboard API base URL in `app.py`
to:

``` python
API_URL = "http://127.0.0.1:5000"
```

For the deployed dashboard, use the Render backend URL:

``` python
API_URL = "https://ai-indoor-navigation.onrender.com"
```

### Android client configuration

Open the Android project in Android Studio, build and install the app on
a compatible phone, grant the required permissions, and set the Flask
API address to the reachable backend URL.

For local testing, the phone and computer must be on a network that
allows the phone to reach the computer's IP address and Flask port. For
deployed testing, use the Render service URL.

## 11. Repository structure

``` text
AI-Indoor-Navigation/
├── dataset/
│   ├── processed/
│   └── WiFi_Final_Dataset.xlsx
├── maps/
│   └── route_visualization.py
├── models/
│   ├── random_forest.pkl
│   └── feature_columns.pkl
├── api.py
├── app.py
├── compare_models.py
├── data_preprocessing.py
├── directions.py
├── evaluate_by_session.py
├── evaluate_model.py
├── location_prediction.py
├── navigation.py
├── standardize_labels.py
├── test_api.py
├── test_navigation_api.py
├── test_prediction.py
├── train_ann.py
├── train_model.py
├── tune_random_forest.py
└── requirements.txt
```

The Android application source is maintained separately from the Python
repository.

## 12. Limitations

-   The dataset contains 102 labelled fingerprints across 10 locations.
-   The held-out offline test contains only 20 fingerprints.
-   Wi-Fi RSSI varies with walls, people, phone orientation,
    interference, access-point load and multipath reflections.
-   Some live scans have low overlap with the trained BSSID set.
-   Live checks were limited and do not establish statistically robust
    accuracy.
-   Route edge weights are approximate; physical route distances require
    on-site measurement.
-   Performance across multiple phone models, days and collection
    conditions has not yet been established.

## 13. Future work

-   Collect more balanced fingerprints at different times, positions and
    phone orientations.
-   Repeat testing across multiple days and devices.
-   Add a low-AP-coverage or low-confidence fallback that asks the user
    to rescan.
-   Validate graph connections, floor transitions and route distances
    on-site.
-   Measure end-to-end latency and route completion rate.
-   Compare localization models using identical session-based evaluation
    splits.

## 14. References

1.  Breiman, L. (2001). Random Forests. *Machine Learning*, 45, 5--32.
2.  Dijkstra, E. W. (1959). A note on two problems in connexion with
    graphs. *Numerische Mathematik*, 1, 269--271.
3.  Android Developers. Wi-Fi scanning and permissions documentation.
4.  Flask Documentation. Flask web framework documentation.
5.  Scikit-learn Documentation. `RandomForestClassifier` and
    classification metrics.

## Contributors

**Project contributors:** 24BCS109, 24BCS071, 24BCS106, 23BCS151.

------------------------------------------------------------------------

*Academic prototype developed for indoor localization and navigation
within the mapped college building.*
