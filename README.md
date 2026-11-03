# AI-Based Indoor Navigation Using Wi-Fi Fingerprinting

A prototype indoor navigation system that uses Wi-Fi fingerprinting and
machine learning to estimate a user's location inside a two-floor
college building, then computes a route to a selected destination.

## Project overview

GPS signals can be attenuated by roofs and walls, making reliable indoor
positioning difficult. This project explores Wi-Fi fingerprinting as an
alternative: the Android application scans nearby Wi-Fi access points,
the backend converts the observed BSSID/RSSI readings into the model's
feature format, and a trained Random Forest classifier predicts one of
the mapped indoor locations. A graph-based navigation module then uses
Dijkstra's algorithm to find a minimum-cost route to the selected
destination.

The prototype combines: - An Android application for Wi-Fi scanning and
destination selection. - A Flask API for receiving scans and returning
predictions and routes. - A Random Forest model for indoor location
classification. - A NetworkX graph with Dijkstra shortest-path
routing. - A Streamlit dashboard for displaying predictions, maps,
routes and walking instructions.

## Live links

-   **Streamlit dashboard:**
    https://ai-indoor-navigation-axpyw4ffwhpq2zjte3acax.streamlit.app
-   **Flask API health check:**
    https://ai-indoor-navigation.onrender.com/health
-   **GitHub repository:**
    https://github.com/rajyalakshmi109/AI-Indoor-Navigation

The dashboard includes a Demo Mode. Live Wi-Fi operation depends on the
deployed API being awake and on receiving a scan from the mapped college
building environment. Render's free service may take some time to wake
after inactivity.

## System workflow

1.  The Android app scans nearby Wi-Fi access points and collects each
    access point's BSSID and RSSI.
2.  The app sends the readings and the selected destination to the Flask
    `/navigate` endpoint.
3.  The backend aligns the readings to the fixed set of 48 trained BSSID
    features. Missing access points are represented as `-100 dBm`.
4.  The Random Forest model predicts the current labelled location and
    returns a confidence estimate.
5.  The navigation module uses Dijkstra's algorithm on the indoor
    connectivity graph to calculate a minimum-cost route.
6.  The API returns the predicted location, destination, route,
    approximate distance and walking instructions.
7.  The Streamlit dashboard can display the prediction, floor map,
    highlighted route and instructions.

## Dataset

The collected dataset contains: - **102 labelled fingerprints** - **10
reference locations** - **2 floors** - **48 BSSID feature columns**

A fingerprint represents one Wi-Fi scan captured at a known location.
BSSID identifies an access point; RSSI is its received signal strength
in dBm.

### Preprocessing and evaluation split

-   Sessions 1 and 2: 82 training fingerprints.
-   Sessions 3 and 4: 20 held-out test fingerprints.
-   All scans are aligned to the same 48 BSSID feature columns.
-   Missing trained access points are represented as `-100 dBm`.

The dataset is relatively small. The held-out test set contains only two
samples per location, so the reported metrics should be interpreted as
preliminary results rather than a definitive measure of building-wide
performance.

## Model and evaluation

Random Forest was selected for the live localization pipeline. An ANN
was also explored separately, but it was not the live model in the
reported test.

### Offline session-based evaluation

-   Correct predictions: **16 out of 20**
-   Accuracy: **80%**
-   Macro precision: **70%**
-   Macro recall: **80%**
-   Macro F1-score: **73.33%**

### Live location checks

During the reported college-building demonstration, **9 of 10** tested
locations were predicted correctly. This is an observed demonstration
result, not a statistically established 90% building-wide accuracy.

Some live scans matched only 1--3 of the 48 trained BSSIDs. Low feature
overlap can reduce prediction reliability, especially when scanning
outside the mapped building or in a different radio environment.

## Navigation

The building is represented as a graph: - Nodes represent mapped indoor
locations. - Edges represent walkable connections. - Edge weights
represent approximate travel distance or cost. - Floor transitions are
represented as graph connections.

Dijkstra's algorithm calculates a minimum-cost path from the predicted
location to the selected destination. Route distances are approximate
graph distances and have not been established as surveyed
physical-distance guarantees.

## Repository structure

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

## Technology stack

-   **Python** --- data processing, machine learning and backend logic
-   **Pandas / NumPy** --- dataset processing
-   **Scikit-learn** --- Random Forest classification and evaluation
-   **Flask** --- REST API
-   **Gunicorn** --- production WSGI server
-   **NetworkX** --- graph representation and shortest-path routing
-   **Streamlit** --- interactive dashboard
-   **Matplotlib** --- floor-map and route visualization
-   **Kotlin / Android** --- mobile Wi-Fi scanning client

## Run locally

### 1. Clone the repository

``` bash
git clone https://github.com/rajyalakshmi109/AI-Indoor-Navigation.git
cd AI-Indoor-Navigation
```

### 2. Create and activate a virtual environment

Windows PowerShell:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Start the Flask API

``` bash
python api.py
```

The API runs locally on port `5000` when started using the project's
development entry point.

### 5. Start the Streamlit dashboard

Open a second terminal, activate the same virtual environment, then run:

``` bash
streamlit run app.py
```

For local live-mode use, configure the dashboard API base URL in
`app.py` to point to the local Flask service (`http://127.0.0.1:5000`).
For the deployed dashboard, the API base URL should point to the Render
service.

## API endpoints

  -----------------------------------------------------------------------
  Method                  Endpoint                Purpose
  ----------------------- ----------------------- -----------------------
  GET                     `/health`               Check whether the API
                                                  is running

  GET                     `/destinations`         Retrieve selectable
                                                  destinations

  POST                    `/predict`              Predict location from
                                                  Wi-Fi readings

  GET                     `/live-location`        Retrieve the latest
                                                  live prediction

  POST                    `/navigate`             Predict location and
                                                  calculate a route to a
                                                  destination
  -----------------------------------------------------------------------

The `/navigate` request contains Wi-Fi readings and a destination. The
Android application sends a JSON object with `scan_readings` and
`destination`.

## Android application

The Android client: 1. Requests the required location/Wi-Fi scan
permissions. 2. Scans nearby Wi-Fi networks. 3. Filters invalid BSSIDs
and RSSI values. 4. Displays detected SSID, BSSID and RSSI information.
5. Sends the scan readings and selected destination to the Flask API. 6.
Displays the returned location prediction and navigation instructions.

For local testing, the phone and computer must be on a network that
allows the phone to reach the computer's IP address and Flask port. For
deployed testing, configure the app's Flask API address to the Render
service URL.

## Limitations

-   The dataset contains 102 fingerprints across 10 locations.
-   The held-out offline test set contains only 20 fingerprints.
-   Wi-Fi RSSI varies with walls, people, device orientation,
    interference, access-point load and multipath effects.
-   Some live scans have low overlap with the trained BSSID set.
-   Live checks were limited and do not establish statistically robust
    accuracy.
-   Route edge weights are approximate; physical route distances require
    on-site measurement.
-   Performance across multiple phone models, days and collection
    conditions has not yet been established.

## Future work

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

## References

1.  Breiman, L. (2001). Random Forests. *Machine Learning*, 45, 5--32.
2.  Dijkstra, E. W. (1959). A note on two problems in connexion with
    graphs. *Numerische Mathematik*, 1, 269--271.
3.  Android Developers --- Wi-Fi scanning and permissions documentation.
4.  Flask Documentation --- Flask web framework.
5.  Scikit-learn Documentation --- `RandomForestClassifier` and
    classification metrics.

## Contributors

Project contributors: 24BCS109, 24BCS071, 24BCS106, 23BCS151.

------------------------------------------------------------------------

This project is an academic prototype developed for indoor localization
and navigation within the mapped college building.
