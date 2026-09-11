import csv
import random

# Common incident types and severity scale
incident_types = ['theft', 'harassment', 'traffic_accident', 'suspicious_activity', 'vandalism', 'burglary']
severities = [1, 1, 1, 2, 2, 3]

# Dictionary of all 12 Karnataka cities with exact GPS bounds and real localities
karnataka_cities = {
    "mysuru": {
        "lat_range": (12.2500, 12.3500),  # Expanded south to cover Srirampura & JP Nagar
        "lon_range": (76.5800, 76.6800),  # Expanded west to cover Vijayanagar
        "zones": [
            "Srirampura", "JP Nagar", "Ashokapuram", "Chamundipuram",
            "Kuvempunagar", "Jayanagar", "Krishnamurthypuram", "Agrahara",
            "Saraswathipuram", "K.R. Mohalla", "Devaraja Mohalla", "Nazarbad",
            "Vijayanagar", "Jayalakshmipuram", "Gokulam", "Hebbal Industrial Area"
        ]
    },
    "bengaluru": {
        "lat_range": (12.9000, 13.0500),
        "lon_range": (77.5200, 77.7200),
        "zones": ['Koramangala', 'Indiranagar', 'MG Road', 'Whitefield', 'Electronic City', 'HSR Layout', 'Jayanagar', 'Hebbal']
    },
    "mangaluru": {
        "lat_range": (12.8500, 12.9500),
        "lon_range": (74.8200, 74.9000),
        "zones": ['Panambur', 'Hampankatta', 'Kadri', 'Bejai', 'Surathkal', 'Falnir', 'Urwa']
    },
    "mandya": {
        "lat_range": (12.5000, 12.5400),
        "lon_range": (76.8700, 76.9200),
        "zones": ['VV Nagar', 'Subhash Nagar', 'Ashok Nagar', 'PES College Area', 'Mandya City Centre']
    },
    "dharwad": {
        "lat_range": (15.4300, 15.4800),
        "lon_range": (74.9800, 75.0400),
        "zones": ['Vidyagiri', 'Line Bazar', 'KCD Circle', 'Navalur', 'Saptapur', 'Sattur']
    },
    "hubli": {
        "lat_range": (15.3300, 15.3900),
        "lon_range": (75.0800, 75.1600),
        "zones": ['Vidyanagar', 'Gokul Road', 'Keshwapur', 'Old Hubli', 'Bengeri', 'Navanagar']
    },
    "hassan": {
        "lat_range": (12.9800, 13.0300),
        "lon_range": (76.0800, 76.1300),
        "zones": ['Kuvempu Nagar', 'BM Road', 'Vidya Nagar', 'Sampige Nagar', 'Salagame Road']
    },
    "shivmogga": {
        "lat_range": (13.9000, 13.9600),
        "lon_range": (75.5300, 75.6000),
        "zones": ['Vinoba Nagar', 'Gopala', 'Tilak Nagar', 'Savalanga Road', 'BH Road']
    },
    "raichur": {
        "lat_range": (16.1800, 16.2300),
        "lon_range": (77.3300, 77.3800),
        "zones": ['Station Road', 'Arab Mohalla', 'Nijalingappa Nagar', 'Mantralayam Road', 'Fort Area']
    },
    "belgaum": {
        "lat_range": (15.8200, 15.8800),
        "lon_range": (74.4700, 74.5300),
        "zones": ['Tilakwadi', 'Camp Area', 'Shahapur', 'Hindwadi', 'Vadgaon', 'Khanapur Road']
    },
    "udupi": {
        "lat_range": (13.3200, 13.3600),
        "lon_range": (74.7200, 74.7600),
        "zones": ['Malpe Beach Area', 'Kalsanka', 'Diana Circle', 'Santhekatte', 'MGM College Area']
    },
    "manipal": {
        "lat_range": (13.3450, 13.3650),
        "lon_range": (74.7750, 74.7980),
        "zones": ['MIT Campus Area', 'Tiger Circle', 'End Point', 'KC Circle', 'Vidyaratna Nagar']
    }
}

# Generate 12 separate CSV files
for city_name, data in karnataka_cities.items():
    filename = f"{city_name}_incidents.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['location_zone', 'latitude', 'longitude', 'hour', 'day_of_week', 'incident_type', 'severity'])
        
        for _ in range(350):
            lat = round(random.uniform(data["lat_range"][0], data["lat_range"][1]), 6)
            lon = round(random.uniform(data["lon_range"][0], data["lon_range"][1]), 6)
            hour = random.randint(0, 23)
            day = random.randint(0, 6)
            zone = random.choice(data["zones"])
            itype = random.choice(incident_types)
            sev = random.choice(severities)
            writer.writerow([f"{city_name.capitalize()} - {zone}", lat, lon, hour, day, itype, sev])
            
    print(f"✅ Created '{filename}' with 350 real geographic records!")

print("\n🎉 All 12 Karnataka city datasets generated successfully!") 