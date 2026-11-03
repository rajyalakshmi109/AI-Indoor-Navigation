# AI-Based Indoor Navigation Using Wi-Fi Fingerprinting

> An academic prototype that estimates a user's location inside a two-floor college building using Wi-Fi fingerprinting and machine learning, then calculates a route to a selected destination.

## Project Overview

GPS signals can be weakened or blocked by roofs and walls, making reliable indoor positioning difficult. This project explores Wi-Fi fingerprinting as an alternative.

The Android application scans nearby Wi-Fi access points and collects their **BSSID** and **RSSI** values. A Flask backend processes these readings and uses a trained **Random Forest classifier** to predict the user's indoor location. A graph-based navigation module then applies **Dijkstra's algorithm** to find a minimum-cost route to the selected destination.

### Main Components

- **Android application:** Scans nearby Wi-Fi access points and lets users select a destination.
- **Flask REST API:** Receives Wi-Fi readings and returns location predictions and navigation routes.
- **Random Forest model:** Classifies the user's current indoor location.
- **Dijkstra navigation:** Calculates a minimum-cost path through the mapped building.
- **Streamlit dashboard:** Displays location predictions, floor maps, routes and walking instructions.

## Live Demo

- **Streamlit dashboard:** https://ai-indoor-navigation-axpyw4ffwhpq2zjte3acax.streamlit.app
- **Flask API health check:** https://ai-indoor-navigation.onrender.com/health
- **GitHub repository:** https://github.com/rajyalakshmi109/AI-Indoor-Navigation

The dashboard includes a Demo Mode. Live Wi-Fi operation requires scans from the mapped college-building environment. The hosted backend may take some time to respond after a period of inactivity because the free service can go to sleep.

## System Workflow

```text
Android application
        |
        | Wi-Fi scan: BSSID + RSSI
        v
     Flask API
        |
        | Validate and align Wi-Fi readings
        v
 Random Forest model
        |
        | Predicted indoor location
        v
 Dijkstra route planning
        |
        | Route, approximate distance,
        | and walking instructions
        v
 Streamlit dashboard / Android app
```

### Workflow Steps

1. The Android application scans nearby Wi-Fi access points and collects their BSSID and RSSI values.
2. The application sends the scan readings and selected destination to the Flask `/navigate` endpoint.
3. The backend aligns the readings to the model's fixed set of 48 BSSID features. Missing access points are represented as `-100 dBm`.
4. The Random Forest model predicts the current labelled location and provides a confidence estimate.
5. The navigation module uses Dijkstra's algorithm on the indoor connectivity graph to calculate a minimum-cost route.
6. The API returns the predicted location, destination, route, approximate distance and walking instructions.
7. The Streamlit dashboard displays the prediction, floor map, highlighted route and directions.

## Dataset

The collected dataset contains:

| Dataset detail | Value |
|---|---:|
| Labelled fingerprints | 102 |
| Reference locations | 10 |
| Floors | 2 |
| BSSID feature columns | 48 |
| Training fingerprints | 82 |
| Held-out test fingerprints | 20 |

A **Wi-Fi fingerprint** is a scan captured at a known location.

- **BSSID:** Identifies a Wi-Fi access point.
- **RSSI:** Represents the received signal strength, measured in dBm.
- **Feature alignment:** Every scan is represented using the same 48 BSSID feature columns.
- **Missing access points:** Represented using `-100 dBm`.
- **Target label:** The known location where the scan was collected.

### Session-Based Train/Test Split

| Collection sessions | Purpose | Number of fingerprints |
|---|---|---:|
| Sessions 1–2 | Training | 82 |
| Sessions 3–4 | Held-out testing | 20 |
| **Total** | | **102** |

The test sessions were kept separate from the training sessions to evaluate the model on later collection sessions rather than randomly mixing scans.

> **Dataset limitation:** The dataset is relatively small. The held-out test set contains only two samples per location, so the reported metrics should be interpreted as preliminary results rather than a definitive measure of building-wide performance.

## Localization Model

A **Random Forest classifier** is used in the live localization pipeline. It predicts one of the labelled indoor locations from the aligned Wi-Fi RSSI fingerprint.

Random Forest is an ensemble learning method that combines predictions from multiple decision trees. It can model non-linear relationships in structured data and provides class-probability estimates that can be used as a confidence indicator.

An Artificial Neural Network (ANN) was also explored separately, but it was not the live model used for the results reported below.

## Navigation Using Dijkstra's Algorithm

The mapped building is represented as a graph:

- **Nodes** represent mapped indoor locations.
- **Edges** represent walkable connections between locations.
- **Edge weights** represent approximate travel distance or cost.
- **Floor transitions** are represented as graph connections.

Dijkstra's algorithm calculates a minimum-cost path from the predicted current location to the selected destination.

### Example Route

```text
Ground Floor Study Hall Centre
              |
              v
Ground Floor Study Hall 2 Entrance
              |
              v
Ground Floor Library Entrance
```

The example route observed during testing was approximately **9 metres** according to the graph. This is an approximate graph distance, not a surveyed physical-distance guarantee.

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Mobile application | Kotlin / Android | Wi-Fi scanning and destination selection |
| Backend | Python / Flask | Receive scans and return predictions and routes |
| Machine learning | Scikit-learn / Random Forest | Indoor location classification |
| Data processing | Pandas / NumPy | Dataset cleaning and transformation |
| Route planning | NetworkX / Dijkstra | Graph-based shortest-path calculation |
| Dashboard | Streamlit | Display predictions, maps and directions |
| Visualization | Matplotlib | Floor-map and route visualization |
| Deployment | Render / Streamlit Community Cloud | Host backend and dashboard |

## Evaluation Results

### Offline Session-Based Evaluation

The Random Forest model was trained using 82 fingerprints from Sessions 1–2 and evaluated using 20 held-out fingerprints from Sessions 3–4.

| Metric | Result |
|---|---:|
| Correct predictions | 16 / 20 |
| Accuracy | **80%** |
| Macro precision | 70% |
| Macro recall | 80% |
| Macro F1-score | 73.33% |

### Live Location Checks

During the reported live college-building demonstration, **9 out of 10** tested locations were predicted correctly. One location was misclassified.

This is an observed demonstration result, not a statistically established 90% building-wide accuracy. It should be considered separately from the offline session-based evaluation.

Some live scans matched only 1–3 of the 48 trained BSSIDs. Low feature overlap can reduce prediction reliability, particularly when scanning outside the mapped building or in a different radio environment.

## API Endpoints

| HTTP method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check whether the API is running |
| `GET` | `/destinations` | Retrieve selectable destinations |
| `POST` | `/predict` | Predict a location from Wi-Fi readings |
| `GET` | `/live-location` | Retrieve the latest live prediction |
| `POST` | `/navigate` | Predict the location and calculate a route |

The Android application sends a JSON request containing `scan_readings` and `destination` to the `/navigate` endpoint.

## Run the Project Locally

### Prerequisites

- Python installed
- Git
- Android Studio (if building or running the Android application)
- A compatible Android phone for live Wi-Fi scanning

### 1. Clone the Repository

```bash
git clone https://github.com/rajyalakshmi109/AI-Indoor-Navigation.git
cd AI-Indoor-Navigation
```

### 2. Create and Activate a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Flask Backend

```bash
python api.py
```

The local development API runs on port `5000` when started using the project's development entry point.

### 5. Start the Streamlit Dashboard

Open a second terminal, activate the same virtual environment, and run:

```bash
streamlit run app.py
```

For local live-mode testing, configure the API base URL in `app.py` as:

```python
API_URL = "http://127.0.0.1:5000"
```

For the deployed dashboard, the API base URL should point to the hosted backend:

```python
API_URL = "https://ai-indoor-navigation.onrender.com"
```

### Android Application Setup

Open the Android project in Android Studio, build and install the application on a compatible phone, grant the required permissions, and configure the Flask API address.

For local testing, the phone and computer must be connected to a network that allows the phone to reach the computer's IP address and Flask port. For deployed testing, configure the application to use the Render service URL.

## Repository Structure

```text
AI-Indoor-Navigation/
├── dataset/
│   ├── processed/
│   └── WiFi_Final_Dataset.xlsx
├── maps/
├── models/
│   ├── random_forest.pkl
│   └── feature_columns.pkl
├── .gitignore
├── README.md
├── api.py
├── app.py
├── compare_models.py
├── data_preprocessing.py
├── directions.py
├── evaluate_by_session.py
├── evaluate_model.py
├── location_prediction.py
├── navigation.py
├── requirements.txt
├── standardize_labels.py
├── test_api.py
├── test_navigation_api.py
├── test_prediction.py
├── train_ann.py
├── train_model.py
└── tune_random_forest.py
```

The Android Studio project is maintained separately from this Python repository.

## Limitations

- The dataset contains 102 fingerprints across 10 reference locations.
- The held-out offline test set contains only 20 fingerprints.
- Wi-Fi RSSI varies with walls, people, device orientation, interference, access-point load and multipath effects.
- Some live scans have low overlap with the trained BSSID set.
- Live checks were limited and do not establish statistically robust accuracy.
- Route edge weights are approximate; physical route distances require on-site measurement.
- Performance across multiple phone models, days and collection conditions has not yet been established.

## Future Work

- Collect more balanced fingerprints at different times, positions and phone orientations.
- Repeat testing across multiple days and devices.
- Add a low-AP-coverage or low-confidence fallback that asks the user to rescan.
- Validate graph connections, floor transitions and route distances on-site.
- Measure end-to-end latency and route completion rate.
- Compare localization models using identical session-based evaluation splits.

## References

1. Breiman, L. (2001). Random Forests. *Machine Learning*, 45, 5–32.
2. Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische Mathematik*, 1, 269–271.
3. Android Developers — Wi-Fi scanning and permissions documentation.
4. Flask Documentation — Flask web framework.
5. Scikit-learn Documentation — `RandomForestClassifier` and classification metrics.

## Contributors

**Project contributors:** 24BCS109, 24BCS071, 24BCS106, 23BCS151.

---

*Academic prototype developed for indoor localization and navigation within the mapped college building.*
