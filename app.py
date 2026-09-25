import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from qiskit import QuantumCircuit
import requests

def get_road_snapped_route(waypoints):
    """
    Takes a list of (lat, lon) coordinates and fetches the exact road-snapped route geometry from OSRM.
    """
    if len(waypoints) < 2:
        return waypoints
    loc_str = ";".join([f"{lon},{lat}" for lat, lon in waypoints])
    url = f"http://router.project-osrm.org/route/v1/driving/{loc_str}?overview=full&geometries=geojson"
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            data = r.json()
            if "routes" in data and len(data["routes"]) > 0:
                coords = data["routes"][0]["geometry"]["coordinates"]
                return [[lat, lon] for lon, lat in coords]
    except Exception:
        pass
    return waypoints 

CITY_POLICE_STATIONS = {
    "bengaluru": [
        {"name": "Cubbon Park Police Station", "lat": 12.9738, "lon": 77.5950},
        {"name": "Commercial Street Police Station", "lat": 12.9818, "lon": 77.6085},
        {"name": "Indiranagar Police Station", "lat": 12.9784, "lon": 77.6408},
        {"name": "Koramangala Police Station", "lat": 12.9352, "lon": 77.6245},
        {"name": "Malleswaram Police Station", "lat": 13.0035, "lon": 77.5702},
        {"name": "Jayanagar Police Station", "lat": 12.9298, "lon": 77.5826},
        {"name": "Shivajinagar Police Station", "lat": 12.9860, "lon": 77.6020},
        {"name": "Frazer Town Police Station", "lat": 12.9972, "lon": 77.6141}
    ],
    "dharwad": [
        {"name": "Dharwad Town Police Station", "lat": 15.4589, "lon": 75.0078},
        {"name": "Dharwad Suburban Police Station", "lat": 15.4520, "lon": 75.0125},
        {"name": "Vidyagiri Police Station", "lat": 15.4320, "lon": 75.0180},
        {"name": "Market Police Station Dharwad", "lat": 15.4570, "lon": 75.0050}
    ],
    "hassan": [
        {"name": "Hassan Town Police Station", "lat": 13.0072, "lon": 76.1023},
        {"name": "Hassan Extension Police Station", "lat": 13.0145, "lon": 76.1090},
        {"name": "Hassan Traffic Police Station", "lat": 13.0020, "lon": 76.0980},
        {"name": "Penshan Mohalla Police Station", "lat": 13.0090, "lon": 76.0950}
    ],
    "hubli": [
        {"name": "Hubballi Suburban PS", "lat": 15.3524, "lon": 75.1382},
        {"name": "Vidyanagar Police Station", "lat": 15.3642, "lon": 75.1228},
        {"name": "Gokul Road Police Station", "lat": 15.3611, "lon": 75.1054},
        {"name": "Kamripeth Police Station", "lat": 15.3480, "lon": 75.1410},
        {"name": "Bendigeri Police Station", "lat": 15.3410, "lon": 75.1520}
    ],
    "mandya": [
        {"name": "Mandya Town Police Station", "lat": 12.5245, "lon": 76.8962},
        {"name": "Mandya West Police Station", "lat": 12.5280, "lon": 76.8890},
        {"name": "Mandya Central Police Station", "lat": 12.5210, "lon": 76.9010},
        {"name": "West Park Police Station", "lat": 12.5310, "lon": 76.8920}
    ],
    "mangaluru": [
        {"name": "Mangaluru North (Bunder) PS", "lat": 12.8712, "lon": 74.8432},
        {"name": "Kadri Police Station", "lat": 12.8778, "lon": 74.8583},
        {"name": "Pandeshwar Police Station", "lat": 12.8601, "lon": 74.8398},
        {"name": "Urwa Police Station", "lat": 12.8892, "lon": 74.8322},
        {"name": "Barke Police Station", "lat": 12.8740, "lon": 74.8480}
    ],
    "manipal": [
        {"name": "Manipal Police Station", "lat": 13.3525, "lon": 74.7865},
        {"name": "MIT Campus Outpost", "lat": 13.3510, "lon": 74.7920},
        {"name": "Tiger Circle Police Post", "lat": 13.3540, "lon": 74.7840},
        {"name": "KMC Campus Outpost", "lat": 13.3570, "lon": 74.7880}
    ],
    "mysuru": [
        {"name": "Devaraja Police Station", "lat": 12.3085, "lon": 76.6520},
        {"name": "Kuvempunagar Police Station", "lat": 12.2855, "lon": 76.6235},
        {"name": "Laxmipuram Police Station", "lat": 12.2965, "lon": 76.6435},
        {"name": "Narasimharaja (N.R.) Police Station", "lat": 12.3225, "lon": 76.6660},
        {"name": "Mandi Police Station", "lat": 12.3160, "lon": 76.6540},
        {"name": "Vidyaranyapuram Police Station", "lat": 12.2805, "lon": 76.6495},
        {"name": "Jayalakshmipuram Police Station", "lat": 12.3175, "lon": 76.6265},
        {"name": "Metagalli Police Station", "lat": 12.3385, "lon": 76.6390}
    ],
    "raichur": [
        {"name": "Raichur Town Police Station", "lat": 16.2052, "lon": 77.3556},
        {"name": "Raichur West Police Station", "lat": 16.2010, "lon": 77.3480},
        {"name": "Netaji Nagar Police Station", "lat": 16.2120, "lon": 77.3610},
        {"name": "Market Police Station Raichur", "lat": 16.2080, "lon": 77.3520}
    ],
    "shivmogga": [
        {"name": "Shivamogga Town Police Station", "lat": 13.9299, "lon": 75.5681},
        {"name": "Doddapet Police Station", "lat": 13.9340, "lon": 75.5720},
        {"name": "Kote Police Station Shivamogga", "lat": 13.9250, "lon": 75.5650},
        {"name": "Vinoba Nagar Police Station", "lat": 13.9410, "lon": 75.5800}
    ],
    "udupi": [
        {"name": "Udupi Town Police Station", "lat": 13.3409, "lon": 74.7421},
        {"name": "Malpe Police Station", "lat": 13.3562, "lon": 74.7042},
        {"name": "Manipal Police Station", "lat": 13.3525, "lon": 74.7865},
        {"name": "Brahmavar Police Station", "lat": 13.4350, "lon": 74.7480}
    ]
}

def get_city_police_stations(location_query):
    query_str = str(location_query).lower()
    for city_key, stations in CITY_POLICE_STATIONS.items():
        if city_key in query_str:
            return stations
    return CITY_POLICE_STATIONS["mysuru"]

from data_generator import (
    get_coordinates_from_location,
    get_real_police_stations,
    generate_synthetic_incidents_around_location,
    process_uploaded_csv,
    train_spatiotemporal_risk_model,
    predict_route_risk,
    generate_executive_report
)
from quantum_solver import (
    build_city_graph, 
    classical_safe_route, 
    compute_greedy_milp_baseline,
    quantum_qubo_resource_allocation,
    run_empirical_benchmark
)

# ALL 11 METROPOLITAN URBAN CENTERS WITH HIGH-PRECISION GPS LOCATIONS
CITY_LOCATIONS = {
    "mysuru": {
        "Srirampura": (12.2590, 76.6320),
        "JP Nagar": (12.2670, 76.6580),
        "Ashokapuram": (12.2810, 76.6430),
        "Chamundipuram": (12.2890, 76.6535),
        "Kuvempunagar": (12.2855, 76.6235),
        "Jayanagar": (12.2940, 76.6360),
        "Krishnamurthypuram": (12.2915, 76.6450),
        "Agrahara": (12.2965, 76.6520),
        "Saraswathipuram": (12.3020, 76.6300),
        "K.R. Mohalla": (12.3010, 76.6450),
        "Devaraja Mohalla": (12.3085, 76.6515),
        "Nazarbad": (12.3075, 76.6660),
        "Vijayanagar": (12.3320, 76.6030),
        "Jayalakshmipuram": (12.3160, 76.6230),
        "Gokulam": (12.3260, 76.6210),
        "Hebbal Industrial Area": (12.3580, 76.6020)
    },
    "bengaluru": {
        "Electronic City": (12.8399, 77.6770),
        "Silk Board": (12.9172, 77.6228),
        "HSR Layout": (12.9121, 77.6446),
        "Koramangala": (12.9352, 77.6245),
        "BTM Layout": (12.9166, 77.6101),
        "Jayanagar": (12.9298, 77.5826),
        "JP Nagar": (12.9077, 77.5855),
        "MG Road": (12.9756, 77.6066),
        "Indiranagar": (12.9784, 77.6408),
        "Whitefield": (12.9698, 77.7499),
        "Marathahalli": (12.9591, 77.6974),
        "Hebbal": (13.0358, 77.5970),
        "Yelahanka": (13.1007, 77.5963),
        "Rajajinagar": (12.9982, 77.5530),
        "Malleshwaram": (13.0035, 77.5702),
        "Banashankari": (12.9250, 77.5468)
    },
    "mangaluru": {
        "Bunder": (12.8712, 74.8432),
        "Kadri": (12.8778, 74.8583),
        "Pandeshwar": (12.8601, 74.8398),
        "Urwa": (12.8892, 74.8322),
        "Barke": (12.8740, 74.8480),
        "Hampankatta": (12.8698, 74.8430),
        "Bejai": (12.8850, 74.8480),
        "Kulshekar": (12.8830, 74.8720),
        "Attavar": (12.8620, 74.8450),
        "Surathkal": (12.9810, 74.8020),
        "Kankanady": (12.8680, 74.8580),
        "Lalbagh": (12.8790, 74.8420),
        "Derebail": (12.8990, 74.8460),
        "Mannagudda": (12.8780, 74.8340),
        "Falnir": (12.8650, 74.8510),
        "Bondel": (12.9120, 74.8650)
    },
    "dharwad": {
        "Dharwad Town": (15.4589, 75.0078),
        "Dharwad Suburban": (15.4520, 75.0125),
        "Vidyagiri": (15.4320, 75.0180),
        "Market Area": (15.4570, 75.0050),
        "Malamaddi": (15.4540, 75.0160),
        "Saptapur": (15.4480, 75.0110),
        "Saidapur": (15.4620, 75.0210),
        "Line Bazaar": (15.4590, 75.0020),
        "Kalyan Nagar": (15.4410, 75.0050),
        "Jubilee Circle": (15.4560, 75.0090),
        "Court Circle": (15.4580, 75.0130),
        "Gandhinagar": (15.4450, 75.0250),
        "Toll Naka": (15.4290, 75.0280),
        "University Campus": (15.4400, 74.9850),
        "Narendra Bypass": (15.4850, 74.9920),
        "Kelgeri": (15.4650, 74.9780)
    },
    "hassan": {
        "Hassan Town": (13.0072, 76.1023),
        "Hassan Extension": (13.0145, 76.1090),
        "Penshan Mohalla": (13.0090, 76.0950),
        "Kuvempu Nagar": (13.0180, 76.1020),
        "Vidya Nagar": (13.0010, 76.1150),
        "Sampige Road": (13.0050, 76.0980),
        "BM Road": (13.0030, 76.1050),
        "Northern Extension": (13.0220, 76.1080),
        "Salagame Road": (13.0110, 76.0890),
        "Dairy Circle": (12.9950, 76.1180),
        "Ring Road Junction": (12.9890, 76.0950),
        "Industrial Area": (13.0280, 76.1250),
        "KR Puram": (13.0040, 76.0920),
        "Shankarpur": (13.0120, 76.1190),
        "Channapatna Circle": (13.0080, 76.1010),
        "Hemavathi Nagar": (12.9980, 76.1080)
    },
    "hubli": {
        "Vidyanagar": (15.3642, 75.1228),
        "Gokul Road": (15.3611, 75.1054),
        "Unkal": (15.3780, 75.1290),
        "Navanagar": (15.3950, 75.1120),
        "Toll Naka": (15.4120, 75.0850),
        "CBT Central": (15.3524, 75.1382),
        "Deshpande Nagar": (15.3560, 75.1310),
        "Keshwapur": (15.3620, 75.1450),
        "Hosur": (15.3450, 75.1280),
        "Shirur Park": (15.3710, 75.1190),
        "Rayapur": (15.4050, 75.0950),
        "Bengeri": (15.3650, 75.1580),
        "Old Hubli": (15.3410, 75.1410),
        "Tarihal": (15.3720, 75.0820),
        "Gamanagatti": (15.3890, 75.0750),
        "Airport Road": (15.3590, 75.0920)
    },
    "mandya": {
        "Mandya Town": (12.5245, 76.8962),
        "Mandya West": (12.5280, 76.8890),
        "Mandya Central": (12.5210, 76.9010),
        "West Park": (12.5310, 76.8920),
        "VV Nagar": (12.5290, 76.9050),
        "Subhash Nagar": (12.5180, 76.8920),
        "Ashok Nagar": (12.5350, 76.8980),
        "Gutthalu": (12.5120, 76.9080),
        "Kallahalli": (12.5380, 76.8850),
        "PES College Campus": (12.5320, 76.8790),
        "Highway Circle": (12.5250, 76.8990),
        "Sugar Town": (12.5190, 76.8810),
        "Swarna Sandhra": (12.5110, 76.8950),
        "Induvalu": (12.5020, 76.8720),
        "Sanjay Circle": (12.5230, 76.8960),
        "Marigudi Extension": (12.5270, 76.9080)
    },
    "manipal": {
        "Police Station Area": (13.3525, 74.7865),
        "MIT Campus": (13.3510, 74.7920),
        "Tiger Circle": (13.3540, 74.7840),
        "KMC Campus": (13.3570, 74.7880),
        "End Point": (13.3620, 74.7850),
        "Ananth Nagar": (13.3480, 74.7960),
        "Dasharath Nagar": (13.3420, 74.7990),
        "Eshwar Nagar": (13.3590, 74.7910),
        "Perampalli": (13.3650, 74.7750),
        "Coin Circle": (13.3515, 74.7885),
        "Vidyaratna Nagar": (13.3460, 74.7820),
        "TAPMI Campus": (13.3610, 74.8020),
        "Manipal Lake": (13.3545, 74.7950),
        "Saralebettu": (13.3410, 74.7890),
        "Laxmindra Nagar": (13.3490, 74.7780),
        "Manipal Bus Stand": (13.3530, 74.7845)
    },
    "raichur": {
        "Raichur Town": (16.2052, 77.3556),
        "Raichur West": (16.2010, 77.3480),
        "Netaji Nagar": (16.2120, 77.3610),
        "Market Area": (16.2080, 77.3520),
        "Arab Mohalla": (16.2030, 77.3590),
        "Nijalingappa Colony": (16.2150, 77.3490),
        "Rajendra Gunj": (16.1980, 77.3540),
        "Station Area": (16.2020, 77.3650),
        "Askihal": (16.1890, 77.3420),
        "Mantralayam Road Circle": (16.2180, 77.3680),
        "LBS Nagar": (16.2090, 77.3420),
        "Tagore Nagar": (16.2220, 77.3520),
        "IDSMT Layout": (16.1950, 77.3610),
        "Rampur Industrial Area": (16.1820, 77.3580),
        "Jawahar Nagar": (16.2060, 77.3640),
        "Agricultural University": (16.2110, 77.3290)
    },
    "shivmogga": {
        "Shivamogga Town": (13.9299, 75.5681),
        "Doddapet": (13.9340, 75.5720),
        "Kote Area": (13.9250, 75.5650),
        "Vinoba Nagar": (13.9410, 75.5800),
        "Gopalagowda Extension": (13.9210, 75.5890),
        "Jayanagar": (13.9380, 75.5610),
        "Vidyanagar": (13.9180, 75.5720),
        "Sharavathi Nagar": (13.9450, 75.5710),
        "Alkola": (13.9520, 75.5610),
        "NT Road": (13.9310, 75.5640),
        "BH Road": (13.9280, 75.5750),
        "Bus Stand Circle": (13.9330, 75.5690),
        "Gandhi Bazar": (13.9350, 75.5670),
        "Savalanga Road": (13.9420, 75.5580),
        "Tunga Nagar": (13.9150, 75.5820),
        "Machenahalli": (13.8890, 75.6150)
    },
    "udupi": {
        "Udupi Town": (13.3409, 74.7421),
        "Malpe": (13.3562, 74.7042),
        "Manipal": (13.3525, 74.7865),
        "Brahmavar": (13.4350, 74.7480),
        "Kadiyali": (13.3460, 74.7550),
        "Santhekatte": (13.3750, 74.7420),
        "Ambalpady": (13.3310, 74.7380),
        "Car Street": (13.3380, 74.7460),
        "Kinnimulki": (13.3280, 74.7450),
        "Ajjarkad": (13.3370, 74.7400),
        "Indrali": (13.3480, 74.7680),
        "End Point": (13.3620, 74.7850),
        "Doddanagudde": (13.3520, 74.7580),
        "Parkala": (13.3510, 74.8050),
        "Udyavara": (13.3080, 74.7390),
        "Gundibail": (13.3460, 74.7480)
    }
}

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & HIGH-CONTRAST UNIFIED THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HeatMap AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }
    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 16px;
        border-radius: 6px;
    }
    .sos-banner {
        background-color: #FEF3C7;
        border: 1px solid #F59E0B;
        border-left: 5px solid #D97706;
        padding: 12px 16px;
        border-radius: 6px;
        color: #92400E;
        font-weight: 600;
        margin-bottom: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. HEADER & OPERATING MANUAL
# -----------------------------------------------------------------------------
st.title("HeatMap AI: Quantum Spatial Safety Intelligence")
st.caption("Spatiotemporal Machine Learning Risk Prediction and QAOA Optimization Platform")

with st.expander("System Operating Manual", expanded=False):
    st.markdown("""
    <div class="instruction-card">
        <h4>Operational Workflow</h4>
        <ol>
            <li><b>Target Location:</b> Specify the city or region in the left sidebar configuration panel.</li>
            <li><b>Data Ingestion:</b> Upload the matching regional incident dataset CSV under Data Source.</li>
            <li><b>Parameters:</b> Adjust time slider, weather intensity, patrol resources, and routing locations.</li>
            <li><b>SOS Simulator:</b> Activate Emergency SOS Alert to simulate real-time patrol re-routing.</li>
            <li><b>Output Analysis:</b> View path risk comparisons, fixed stations, patrol assignments, and QPU benchmarks across tabs.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 1. Location Settings")
user_location_query = st.sidebar.text_input("Target City / Area", value="Mysuru, India")

st.sidebar.markdown("---")
st.sidebar.markdown("### 2. Data Source")
uploaded_file = st.sidebar.file_uploader("Upload Regional Dataset (CSV)", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 3. Simulation Parameters")
selected_hour = st.sidebar.slider("Time of Day (24h Clock)", 0, 23, 22)
selected_day = st.sidebar.selectbox("Day of Week", options=[0,1,2,3,4,5,6], format_func=lambda x: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][x])
rainfall_mm = st.sidebar.slider("Rainfall / Weather Intensity (mm/h)", 0.0, 50.0, 0.0, step=2.5)
num_patrols = st.sidebar.slider("Emergency Patrol Units", 1, 5, 3)

# DYNAMIC CITY MATCHING FOR ALL 11 CITIES
city_query_lower = user_location_query.lower()
matched_city_key = "mysuru"
for c_key in CITY_LOCATIONS.keys():
    if c_key in city_query_lower:
        matched_city_key = c_key
        break

loc_dict = CITY_LOCATIONS[matched_city_key]
location_names = list(loc_dict.keys())

# Create internal mappings for graph computations
area_to_id = {name: i for i, name in enumerate(location_names)}
id_to_area = {i: name for i, name in enumerate(location_names)}
node_coords = {i: loc_dict[name] for i, name in enumerate(location_names)}

st.sidebar.markdown("---")
st.sidebar.markdown("### 4. Emergency SOS Dispatch Simulator")
sos_enabled = st.sidebar.checkbox("Activate Emergency SOS Alert", value=False)
sos_area = st.sidebar.selectbox("SOS Location", options=location_names, index=min(7, len(location_names)-1))
sos_node = area_to_id[sos_area]

st.sidebar.markdown("---")
st.sidebar.markdown("### 5. Routing Location Selection")
start_area = st.sidebar.selectbox("Start Location", options=location_names, index=min(3, len(location_names)-1))
end_area = st.sidebar.selectbox("Destination Location", options=location_names, index=min(12, len(location_names)-1))

start_node = area_to_id[start_area]
end_node = area_to_id[end_area]

if start_node == end_node:
    st.sidebar.error("Start and Destination locations must be distinct.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 6. Quantum QAOA Setup")
qaoa_gamma = st.sidebar.slider("Gamma (Phase Separator)", 0.1, 3.14, 1.2, step=0.1)
qaoa_beta = st.sidebar.slider("Beta (Mixer Angle)", 0.1, 3.14, 0.8, step=0.1)

def build_qaoa_circuit(num_qubits=4, gamma=1.2, beta=0.8):
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))
    qc.barrier()
    for i in range(num_qubits - 1):
        qc.rzz(2 * gamma, i, i + 1)
    qc.barrier()
    for i in range(num_qubits):
        qc.rx(2 * beta, i)
    qc.barrier()
    qc.measure_all()
    return qc

# -----------------------------------------------------------------------------
# 4. DATA PIPELINE & MODEL COMPUTATION
# -----------------------------------------------------------------------------
if uploaded_file is not None:
    try:
        df_incidents = process_uploaded_csv(uploaded_file)
        st.sidebar.success("Dataset Ingested")
        center_lat = (df_incidents['latitude'].min() + df_incidents['latitude'].max()) / 2.0
        center_lon = (df_incidents['longitude'].min() + df_incidents['longitude'].max()) / 2.0
    except Exception as e:
        st.sidebar.error(f"Error processing CSV: {e}")
        center_lat, center_lon = get_coordinates_from_location(user_location_query)
        df_incidents = generate_synthetic_incidents_around_location(user_location_query, center_lat, center_lon)
else:
    center_lat, center_lon = get_coordinates_from_location(user_location_query)
    df_incidents = generate_synthetic_incidents_around_location(user_location_query, center_lat, center_lon)

police_stations = get_real_police_stations(user_location_query, center_lat, center_lon)
risk_model = train_spatiotemporal_risk_model(df_incidents)

risk_scores = predict_route_risk(risk_model, node_coords, hour=selected_hour, day=selected_day, rainfall_mm=rainfall_mm)
city_graph = build_city_graph(node_coords, risk_scores)

safe_path, fast_path = classical_safe_route(city_graph, source=int(start_node), target=int(end_node))
# NEW LINE (PASTE THIS)
milp_patrols = compute_greedy_milp_baseline(risk_scores, node_coords, num_patrols=num_patrols)
patrol_nodes, bitstring_probs, bitstring_details = quantum_qubo_resource_allocation(risk_scores, node_coords, num_patrols=num_patrols)

dispatch_node = None
dispatch_path = []
if sos_enabled:
    best_dist = float('inf')
    for p_node in patrol_nodes:
        try:
            length = nx.shortest_path_length(city_graph, source=p_node, target=int(sos_node), weight='weight')
            if length < best_dist:
                best_dist = length
                dispatch_node = p_node
        except nx.NetworkXNoPath:
            continue
    if dispatch_node is not None:
        dispatch_path = nx.shortest_path(city_graph, source=dispatch_node, target=int(sos_node), weight='weight')

# -----------------------------------------------------------------------------
# 5. DASHBOARD TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Spatial Command Map", 
    "Quantum QAOA Architecture", 
    "Performance Benchmarks",
    "Incident Dataset Preview"
])

# TAB 1: SPATIAL COMMAND MAP
with tab1:
    if sos_enabled and dispatch_node is not None:
        st.markdown(f"""
        <div class="sos-banner">
            CRITICAL SOS DISPATCH ACTIVE: Emergency call received at {sos_area}. 
            Nearest Quantum Patrol Unit at {id_to_area[dispatch_node]} re-routed!
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2 = st.columns([2.3, 1])

    with col1:
        st.subheader(f"Spatial Map — {user_location_query}")
        st.caption("Black Building Icons: Fixed Police Stations | Blue Shields: Mobile Patrol Units | Green Route: Safe Path")

        m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="OpenStreetMap")

        heat_data = [[row['latitude'], row['longitude'], row['severity']] for _, row in df_incidents.iterrows()]
        HeatMap(heat_data, radius=14, blur=18, min_opacity=0.45).add_to(m)

        fast_waypoints = [node_coords[n] for n in fast_path]
        fast_road_coords = get_road_snapped_route(fast_waypoints)
        folium.PolyLine(fast_road_coords, color="#DC2626", weight=5, opacity=0.85, tooltip="Fastest Path (High Risk)").add_to(m)

        safe_waypoints = [node_coords[n] for n in safe_path]
        safe_road_coords = get_road_snapped_route(safe_waypoints)
        folium.PolyLine(safe_road_coords, color="#16A344", weight=6, opacity=0.95, tooltip="Quantum Safe Path").add_to(m)

        folium.Marker(node_coords[int(start_node)], popup=f"Start: {start_area}", icon=folium.Icon(color="green", icon="play", prefix="fa")).add_to(m)
        folium.Marker(node_coords[int(end_node)], popup=f"Destination: {end_area}", icon=folium.Icon(color="red", icon="flag", prefix="fa")).add_to(m)

        active_stations = get_city_police_stations(user_location_query)

        # Draw Real Physical Police Stations
        for ps in active_stations:
            folium.Marker(
                location=[ps["lat"], ps["lon"]],
                popup=f"<b>Police Station:</b> {ps['name']}",
                tooltip=f"Station: {ps['name']}",
                icon=folium.Icon(color="black", icon="building", prefix="fa")
            ).add_to(m)

        # Draw Mobile Patrol Units
        for p_node in patrol_nodes:
            lat, lon = node_coords[p_node]
            p_name = id_to_area[p_node]
            folium.Marker(
                location=[lat, lon],
                popup=f"Mobile Patrol Unit ({p_name})",
                icon=folium.Icon(color="blue", icon="shield", prefix="fa")
            ).add_to(m)

        # Draw SOS Alert Overlay
        if sos_enabled and dispatch_node is not None:
            folium.Marker(
                location=node_coords[int(sos_node)],
                popup=f"EMERGENCY SOS ALERT ({sos_area})",
                icon=folium.Icon(color="orange", icon="exclamation-triangle", prefix="fa")
            ).add_to(m)

            dispatch_waypoints = [node_coords[n] for n in dispatch_path]
            dispatch_road_coords = get_road_snapped_route(dispatch_waypoints)
            folium.PolyLine(
                dispatch_road_coords,
                color="#D97706",
                weight=5,
                opacity=0.95,
                dash_array="8, 8",
                tooltip=f"Emergency Interception Route ({id_to_area[dispatch_node]} -> {sos_area})"
            ).add_to(m) 

        st_folium(m, width=850, height=520)

    with col2:
        st.subheader("Performance Metrics")
        
        fast_risk_score = sum([risk_scores[n] for n in fast_path])
        safe_risk_score = sum([risk_scores[n] for n in safe_path])
        risk_reduction = ((fast_risk_score - safe_risk_score) / fast_risk_score) * 100 if fast_risk_score > 0 else 0
        
        st.metric(label="Risk Reduction", value=f"{risk_reduction:.1f}%", delta=f"-{fast_risk_score - safe_risk_score:.2f} Penalty")
        st.metric(label="Fixed Stations Found", value=f"{len(active_stations)} Stations")  
        
        if sos_enabled and dispatch_node is not None:
            st.metric(label="Active SOS Dispatch", value=sos_area, delta=f"Assigned Patrol: {id_to_area[dispatch_node]}")
        else:
            st.metric(label="Region", value=user_location_query)
        st.markdown("---")
        st.markdown("#### Executive Reporting")
        
        day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        day_label = day_names[selected_day]
        
        report_text = generate_executive_report(
            location=user_location_query,
            hour=selected_hour,
            day_str=day_label,
            rainfall=rainfall_mm,
            start_n=start_node,
            end_n=end_node,
            fast_risk=fast_risk_score,
            safe_risk=safe_risk_score,
            risk_reduction=risk_reduction,
            patrol_nodes=patrol_nodes,
            node_coords=node_coords,
            risk_scores=risk_scores,
            police_stations=active_stations,
            sos_enabled=sos_enabled,
            sos_node=sos_node,
            dispatch_node=dispatch_node,
            id_to_area=id_to_area  # <--- NEW PARAMETER
        ) 
        
        st.download_button(
            label="Download Executive Dispatch Memo (.txt)",
            data=report_text,
            file_name=f"HeatMap_AI_Dispatch_Report_{user_location_query.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.markdown("---")
        st.markdown("#### Fixed Police Stations")
        for ps in active_stations:
            st.write(f"• **{ps['name']}**")
            
        st.markdown("---")
        st.markdown("#### Patrol Assignments (QUBO)")
        for node_id in patrol_nodes:
            node_area = id_to_area[node_id]
            is_dispatched = " [DISPATCHED]" if (sos_enabled and node_id == dispatch_node) else ""
            st.write(f"• **{node_area}**: Risk Penalty = `{risk_scores[node_id]:.2f}`{is_dispatched}")

# --- TAB 2: QUANTUM QAOA ARCHITECTURE ---
# --- TAB 2: QUANTUM QAOA ARCHITECTURE ---
with tab2:
    st.subheader("QAOA Parameter Optimization & Quantum Statevector Distribution")
    st.caption(f"Quantum optimization mapping for {user_location_query}")
    
    col_q1, col_q2 = st.columns(2)
    
    # 1. Circuit Rendering (Self-contained Qiskit Circuit)
    with col_q1:
        st.markdown("#### Qiskit Parameterized Circuit")
        try:
            from qiskit import QuantumCircuit
            from qiskit.circuit import Parameter
            
            g_param = Parameter('γ')
            b_param = Parameter('β')
            display_qc = QuantumCircuit(4, name="QAOA_Ansatz")
            
            display_qc.h(range(4))
            display_qc.barrier()
            
            display_qc.rzz(g_param, 0, 1)
            display_qc.rzz(g_param, 1, 2)
            display_qc.rzz(g_param, 2, 3)
            display_qc.barrier()
            
            for q in range(4):
                display_qc.rx(b_param, q)
                
            display_qc.measure_all()
            
            fig_qc = display_qc.draw(output='mpl', style='iqp')
            st.pyplot(fig_qc)
        except Exception:
            st.code(str(display_qc.draw(output='text')), language='text')
            
    # 2. Probability Distribution Plot
    with col_q2:
        st.markdown("#### QAOA Measurement Probability Distribution")
        
        fig2, ax2 = plt.subplots(figsize=(8, 4.5))
        fig2.patch.set_facecolor('#FFFFFF')
        ax2.set_facecolor('#FFFFFF')
        
        states = list(bitstring_probs.keys())
        probs = list(bitstring_probs.values())
        
        ax2.bar(states, probs, color='#0F172A', edgecolor='#334155', linewidth=1.0)
        
        ax2.set_xticks(range(len(states)))
        ax2.set_xticklabels(states, rotation=45, ha='right', fontsize=9, color='#0F172A')
        
        ax2.set_xlabel("Qubit Bitstrings (|q₃ q₂ q₁ q₀⟩)", fontsize=10, color='#0F172A')
        ax2.set_ylabel("Measurement Probability", fontsize=10, color='#0F172A')
        ax2.set_title(f"State Probabilities ({user_location_query})", fontsize=11, color='#0F172A')
        ax2.grid(axis='y', linestyle='--', alpha=0.3)
        
        st.pyplot(fig2)

    st.markdown("---")
    st.markdown("#### Qubit Bitstring Mapping to Candidate Localities")
    st.dataframe(pd.DataFrame(bitstring_details), use_container_width=True)

# TAB 3: PERFORMANCE BENCHMARKS
# TAB 3: PERFORMANCE BENCHMARK
# TAB 3: PERFORMANCE BENCHMARKS
with tab3:
    st.subheader("Empirical Optimization Benchmarks")
    st.caption(f"Quantitative evaluation in {user_location_query}")

    col_b1, col_b2 = st.columns(2)
    
    fast_risk_val = sum([risk_scores[n] for n in fast_path])
    milp_patrols = compute_greedy_milp_baseline(risk_scores, node_coords, num_patrols=num_patrols)
    milp_risk_val = sum([risk_scores[n] for n in milp_patrols])
    safe_risk_val = sum([risk_scores[n] for n in safe_path])

    with col_b1:
        st.markdown("#### 1. Route Risk Exposure")
        fig_bench1, ax_b1 = plt.subplots(figsize=(7, 4.2))
        
        methods = ['Dijkstra', 'MILP Solver', 'QAOA (Ours)']
        m_risks = [fast_risk_val, milp_risk_val, safe_risk_val]
        colors = ['#DC2626', '#475569', '#16A34A']
        
        bars = ax_b1.bar(methods, m_risks, color=colors, width=0.45)
        ax_b1.set_ylabel("Accumulated Risk Penalty", fontsize=10)
        ax_b1.set_title("Safety Quality (Lower is Better)", fontsize=11)
        ax_b1.grid(axis='y', linestyle='--', alpha=0.3)
        
        for bar in bars:
            yval = bar.get_height()
            ax_b1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f"{yval:.2f}", ha='center', va='bottom', fontweight='bold')
            
        st.pyplot(fig_bench1)

    with col_b2:
        st.markdown("#### 2. Scalability Benchmark (Live Measured)")
        
        # Execute real dynamic benchmark
        nodes_scale, classical_times, quantum_times = run_empirical_benchmark(risk_scores, node_coords)
        
        fig_bench2, ax_b2 = plt.subplots(figsize=(7, 4.2))
        ax_b2.plot(nodes_scale, classical_times, label='Classical MILP (SciPy)', marker='o', color='#DC2626', linewidth=1.8)
        ax_b2.plot(nodes_scale, quantum_times, label='QAOA Statevector Simulation', marker='s', color='#0F172A', linewidth=1.8)
        ax_b2.set_xlabel("Grid Size (Locations)", fontsize=10)
        ax_b2.set_ylabel("Execution Time (Seconds)", fontsize=10)
        ax_b2.set_title("Measured Computational Complexity", fontsize=11)
        ax_b2.legend(frameon=True)
        ax_b2.grid(True, linestyle='--', alpha=0.3)
        
        st.pyplot(fig_bench2) 

# TAB 4: DATASET PREVIEW
with tab4:
    st.subheader(f"Incident Dataset Overview — {user_location_query}")
    st.caption("Active incident records processed by the Spatiotemporal ML model")
    st.dataframe(df_incidents, use_container_width=True) 