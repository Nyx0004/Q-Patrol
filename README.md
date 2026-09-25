# Q-Patrol
### Quantum-Assisted Police Patrol Optimization & Emergency Dispatch System

Q-Patrol is a GIS-based police patrol planning and emergency dispatch prototype that combines **QUBO optimization, QAOA, spatial risk analysis, and real-world road routing**.

The system is designed to explore how limited mobile patrol units can be distributed across different city locations based on risk levels, while also supporting road-based routing and emergency SOS response.

> **Live Demo:** [Open Q-Patrol on Streamlit](https://q-patrol-8fkub75ctfkzzc2nlovehq.streamlit.app/)

---

## Overview

Police departments have limited patrol units, while different areas of a city can have different levels of risk.

Q-Patrol addresses this problem by combining:

- **Spatial risk analysis** to represent risk across locations
- **QUBO** to mathematically model patrol allocation
- **QAOA** to explore possible patrol configurations
- **OSRM** for real-world road-based routing
- **SOS dispatch logic** to identify and route the nearest patrol
- **GIS visualization** to display locations, risk, patrols, and routes

The goal is to create a single interactive platform for experimenting with **patrol optimization and emergency response planning**.

---

# Key Features

## 1. Spatial Risk Analysis

Q-Patrol works with city-specific datasets containing location, coordinate, and risk information.

The system uses these values to visualize spatial risk across the selected city.

Example:


Location          Risk Score
----------------------------
Devaraja             0.82
Mandi                0.91
Laxmipuram           0.71
Kuvempunagar         0.64
Metagalli            0.48

## 2. QUBO-Based Patrol Optimization

The patrol allocation problem is formulated as a **QUBO**.

QUBO stands for:

**Quadratic Unconstrained Binary Optimization**

Each location is represented using a binary decision variable:


xᵢ = 1  → Patrol assigned
xᵢ = 0  → No patrol

The optimization model considers:

Location risk
Spatial proximity between patrol assignments
Required number of patrol units

The objective is to identify patrol configurations with lower QUBO energy.

Conceptually:
High-risk location
        ↓
Higher patrol priority

Patrols too close
        ↓
Penalty

Incorrect patrol count
        ↓
Penalty

# 3. QAOA Quantum Optimization

QAOA stands for:

**Quantum Approximate Optimization Algorithm**

QAOA is used to explore possible solutions to the QUBO patrol allocation problem.

The QUBO is converted into an **Ising Hamiltonian**, which is then represented using a Qiskit quantum circuit.

The QAOA circuit uses two important parameters:

### Gamma (γ)

Controls how strongly the quantum circuit follows the cost function.

### Beta (β)

Controls the mixing and exploration between possible solutions.

The circuit produces a probability distribution over possible patrol configurations.

### Current Quantum Implementation

The current implementation uses a **4-qubit QAOA statevector simulation** through Qiskit.

This means the quantum circuit is simulated on a classical computer rather than executed on a physical quantum processing unit.

# 4. Real-World Road Routing

Q-Patrol uses the **Open Source Routing Machine (OSRM)** to calculate routes using actual road-network geometry.

Instead of relying only on straight-line distance, the system obtains road-based route geometry.

The routing component supports:

- Fastest route calculation
- Risk-weighted route calculation
- Patrol-to-emergency routing
- Road-snapped route visualization

Example workflow:


Patrol Location
       ↓
OSRM Routing Engine
       ↓
Road Network
       ↓
Destination
       ↓
Route displayed on map


# 5. Emergency SOS Dispatch

Q-Patrol includes an SOS dispatch workflow for emergency response.

When an SOS event is triggered, the system:


SOS Alert
    ↓
Identify Available Patrol
    ↓
Find Nearest Patrol Unit
    ↓
Calculate Road Route
    ↓
Display Dispatch Path

# 6. Multi-City Support

Q-Patrol supports multiple city datasets and dynamically updates the spatial information when the selected city changes.

Currently configured cities include:

- Bengaluru
- Mysuru
- Mangaluru
- Dharwad
- Hassan
- Hubballi
- Mandya
- Manipal
- Raichur
- Shivamogga
- Udupi

Each city contains location-specific spatial and risk data.

# 7. GIS Visualization

The application provides an interactive map-based command-center interface.

The map can be used to visualize:

- Risk locations
- Police stations
- Patrol assignments
- Emergency locations
- Calculated routes
- Spatial coverage information

The interface is built using **Streamlit** with **Folium/Leaflet-based mapping**.

# 8. Executive Incident Report

Q-Patrol can generate a structured `.txt` incident report summarizing the results of the analysis.

The report can include:

- Selected patrol locations
- Risk information
- Patrol assignments
- Spatial metrics
- Route information
- Emergency dispatch details

This provides a simple, structured record of the analysis and decisions generated by the system.




  # Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Interactive command-center interface |
| Mapping | Folium / Leaflet.js | GIS visualization and route rendering |
| Routing | OSRM API | Road-based route calculation |
| Quantum Computing | Qiskit | QAOA circuit construction and simulation |
| Optimization | QUBO | Patrol allocation model |
| Classical Optimization | SciPy MILP | Classical optimization baseline |
| Data Processing | Pandas / NumPy | Risk and spatial data processing |
| Graph Processing | NetworkX | Spatial graph processing |
| Language | Python | Core implementation |

---

# Mathematical Model

The patrol allocation problem uses binary decision variables:


xᵢ ∈ {0, 1}
where:
xᵢ = 1 → Patrol assigned
xᵢ = 0 → No patrol

# The QUBO combines multiple factors:

Risk

Higher-risk locations are given greater priority in the patrol allocation objective.

Spatial Proximity

A penalty discourages excessive concentration of patrol units in nearby locations.

Patrol Count

A penalty encourages the solution to select the required number of patrol units.

The resulting QUBO is converted into an Ising representation and used to construct the QAOA circuit.


# Classical Baseline

The project also includes a classical Mixed-Integer Linear Programming (MILP) baseline using SciPy.

The classical optimization provides a reference point for comparing the patrol allocation process.

The system can examine:

Patrol allocation
Execution time
Problem size
Optimization behavior

The QAOA implementation currently operates as a 4-qubit statevector simulation on a classical computer. Therefore, the project demonstrates the QAOA workflow and quantum optimization formulation without claiming execution on physical quantum hardware.


# Installation

1. Clone the Repository
git clone https://github.com/Nyx0004/Q-Patrol
cd Q-Patrol

2. Create a Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
streamlit run app.py

The application will open in your browser.

Live Demo

The project is deployed using Streamlit Community Cloud.

# 🔗 Live Application:

https://q-patrol-8fkub75ctfkzzc2nlovehq.streamlit.app/

The live demo allows users to interact with the GIS interface, explore city datasets, run the optimization workflow, view routes, and test the SOS dispatch functionality.
