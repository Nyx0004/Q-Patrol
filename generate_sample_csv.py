import csv
import random

num_records = 350
incident_types = ['theft', 'harassment', 'traffic_accident', 'suspicious_activity', 'vandalism', 'burglary']
severities = [1, 1, 1, 2, 2, 3]

# Complete list of all 16 Mysuru neighborhoods
MYSURU_LOCALITIES = [
    "Srirampura", "JP Nagar", "Ashokapuram", "Chamundipuram",
    "Kuvempunagar", "Jayanagar", "Krishnamurthypuram", "Agrahara",
    "Saraswathipuram", "K.R. Mohalla", "Devaraja Mohalla", "Nazarbad",
    "Vijayanagar", "Jayalakshmipuram", "Gokulam", "Hebbal Industrial Area"
]

# Coordinate mapping bounding boxes for each locality
LOCALITY_COORDS = {
    "Srirampura": (12.2600, 76.6150),
    "JP Nagar": (12.2650, 76.6320),
    "Ashokapuram": (12.2720, 76.6450),
    "Chamundipuram": (12.2800, 76.6580),
    "Kuvempunagar": (12.2850, 76.6200),
    "Jayanagar": (12.2900, 76.6350),
    "Krishnamurthypuram": (12.2920, 76.6480),
    "Agrahara": (12.2950, 76.6550),
    "Saraswathipuram": (12.3020, 76.6250),
    "K.R. Mohalla": (12.3000, 76.6420),
    "Devaraja Mohalla": (12.3080, 76.6500),
    "Nazarbad": (12.3100, 76.6650),
    "Vijayanagar": (12.3250, 76.6100),
    "Jayalakshmipuram": (12.3180, 76.6280),
    "Gokulam": (12.3300, 76.6380),
    "Hebbal Industrial Area": (12.3400, 76.6500)
}

with open('incidents.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header matching app expectations
    writer.writerow([
        'location_zone', 'latitude', 'longitude', 
        'hour', 'day_of_week', 'incident_type', 'severity', 'rainfall_mm'
    ])

    for _ in range(num_records):
        locality = random.choice(MYSURU_LOCALITIES)
        base_lat, base_lon = LOCALITY_COORDS[locality]
        
        # Add slight spatial variation around each neighborhood center
        lat = round(base_lat + random.uniform(-0.005, 0.005), 6)
        lon = round(base_lon + random.uniform(-0.005, 0.005), 6)
        
        hour = random.randint(0, 23)
        day = random.randint(0, 6)
        itype = random.choice(incident_types)
        sev = random.choice(severities)
        rainfall = round(random.uniform(0.0, 30.0), 4)

        writer.writerow([
            f"Mysuru - {locality}", lat, lon, hour, day, itype, sev, rainfall
        ])

print("✅ Successfully generated 'incidents.csv' with 350 records covering all 16 Mysuru localities!") 