import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="heatmap_ai_app")

def get_coordinates_from_location(location_name):
    try:
        location = geolocator.geocode(location_name, timeout=5)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    # Default fallback (Mysuru coordinates)
    return 12.3118, 76.6529

def get_real_police_stations(location_name, center_lat, center_lon):
    """Fetch physical police station locations via OpenStreetMap Nominatim API."""
    try:
        query = f"police station in {location_name}"
        locations = geolocator.geocode(query, exactly_one=False, limit=4, timeout=5)
        stations = []
        if locations:
            for loc in locations:
                stations.append({
                    'name': loc.address.split(',')[0],
                    'lat': loc.latitude,
                    'lon': loc.longitude
                })
            return stations
    except Exception:
        pass
    
    # Anchor fallback locations around city center if API limit is reached
    return [
        {'name': f"Central Police Station ({location_name})", 'lat': center_lat + 0.006, 'lon': center_lon - 0.005},
        {'name': f"Traffic & Security Sub-Division", 'lat': center_lat - 0.007, 'lon': center_lon + 0.006},
        {'name': f"North Division Police HQ", 'lat': center_lat + 0.011, 'lon': center_lon + 0.003}
    ]

def generate_synthetic_incidents_around_location(location_name, center_lat, center_lon, num_records=350):
    np.random.seed(42)
    lats = np.random.normal(loc=center_lat, scale=0.015, size=num_records)
    lons = np.random.normal(loc=center_lon, scale=0.015, size=num_records)
    hours = np.random.randint(0, 24, size=num_records)
    days = np.random.randint(0, 7, size=num_records)
    rainfalls = np.random.uniform(0.0, 45.0, size=num_records)
    
    base_severity = np.random.choice([1, 2, 3], size=num_records)
    night_factor = np.where((hours >= 20) | (hours <= 4), 1.3, 1.0)
    weather_factor = 1.0 + (rainfalls / 50.0)
    
    severities = np.clip(np.round(base_severity * night_factor * weather_factor), 1, 5)
    
    df = pd.DataFrame({
        'latitude': lats,
        'longitude': lons,
        'hour': hours,
        'day_of_week': days,
        'rainfall_mm': rainfalls,
        'severity': severities
    })
    return df

def process_uploaded_csv(file):
    df = pd.read_csv(file)
    required_cols = {'latitude', 'longitude', 'hour', 'day_of_week', 'severity'}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError("CSV missing required columns: latitude, longitude, hour, day_of_week, severity")
    
    if 'rainfall_mm' not in df.columns:
        np.random.seed(42)
        df['rainfall_mm'] = np.random.uniform(0.0, 30.0, size=len(df))
        
    return df

def train_spatiotemporal_risk_model(df):
    X = df[['latitude', 'longitude', 'hour', 'day_of_week', 'rainfall_mm']]
    y = df['severity']
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    return model

def predict_route_risk(model, node_coords, hour=22, day=4, rainfall_mm=0.0):
    risk_scores = {}
    for node_id, (lat, lon) in node_coords.items():
        input_data = pd.DataFrame({
            'latitude': [lat],
            'longitude': [lon],
            'hour': [hour],
            'day_of_week': [day],
            'rainfall_mm': [rainfall_mm]
        })
        predicted_risk = model.predict(input_data)[0]
        risk_scores[node_id] = float(predicted_risk)
    return risk_scores 
def find_nearest_node(address_text, node_coords, default_node=0):
    """Geocodes an address string and finds the closest grid node ID."""
    try:
        location = geolocator.geocode(address_text, timeout=5)
        if location:
            target_lat, target_lon = location.latitude, location.longitude
            closest_node = min(
                node_coords.keys(),
                key=lambda n: (node_coords[n][0] - target_lat)**2 + (node_coords[n][1] - target_lon)**2
            )
            return closest_node
    except Exception:
        pass
    return default_node
import pandas as pd

def generate_executive_report(location, hour, day_str, rainfall, start_n, end_n, fast_risk, safe_risk, risk_reduction, patrol_nodes, node_coords, risk_scores, police_stations, sos_enabled, sos_node, dispatch_node):
    report = f"""================================================================================
                HEATMAP AI — EXECUTIVE INCIDENT & DISPATCH MEMO
================================================================================
Generated Timestamp : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Sector / City: {location}
System Status       : OPERATIONAL / ACTIVE

--------------------------------------------------------------------------------
1. ENVIRONMENTAL & SPATIOTEMPORAL CONTEXT
--------------------------------------------------------------------------------
• Target Time Window    : {hour}:00 Hours ({day_str})
• Weather Factor        : {rainfall} mm/h Precipitation Intensity
• Machine Learning Model: Spatiotemporal Random Forest Regressor

--------------------------------------------------------------------------------
2. ROUTE RISK EVALUATION & OPTIMIZATION
--------------------------------------------------------------------------------
• Origin Node ID        : Node {start_n}
• Destination Node ID   : Node {end_n}
• Classical Shortest Path Risk Penalty: {fast_risk:.2f}
• Quantum Safe Path Accumulated Risk  : {safe_risk:.2f}
• Total Exposure Reduction Factor     : {risk_reduction:.1f}%

--------------------------------------------------------------------------------
3. QUANTUM ALLOCATION (QUBO PATROL UNITS)
--------------------------------------------------------------------------------
Total Mobile Patrol Units Deployed: {len(patrol_nodes)}
"""
    for n in patrol_nodes:
        lat, lon = node_coords[n]
        report += f"  - Patrol Unit at Node {n:02d} | Coordinates: ({lat:.4f}, {lon:.4f}) | Local Risk Score: {risk_scores[n]:.2f}\n"

    if sos_enabled and dispatch_node is not None:
        report += f"""
--------------------------------------------------------------------------------
4. EMERGENCY SOS DISPATCH ALERT LOG
--------------------------------------------------------------------------------
• ALERT STATUS          : CRITICAL / ACTIVE
• SOS Incident Location : Node {sos_node}
• Re-routed Patrol Unit : Patrol Unit at Node {dispatch_node}
"""

    report += f"""
--------------------------------------------------------------------------------
5. SECTOR PHYSICAL POLICE STATIONS
--------------------------------------------------------------------------------
"""
    for st_info in police_stations:
        report += f"  - {st_info['name']} (Lat: {st_info['lat']:.4f}, Lon: {st_info['lon']:.4f})\n"

    report += """
================================================================================
CONFIDENTIAL — MUNICIPAL PUBLIC SAFETY COMMAND CENTER
================================================================================
"""
    return report