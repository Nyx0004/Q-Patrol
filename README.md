# Q-Patrol

### Quantum-Assisted Police Patrol Optimization & Emergency Dispatch System

Q-Patrol is a GIS-based police patrol planning and emergency dispatch prototype that combines **QUBO-based optimization, QAOA, spatial risk analysis, and real-world road routing**.

The system helps determine where limited mobile patrol units can be deployed based on spatial risk data and provides road-based routing for patrol movement and emergency SOS response.

---

## What Problem Does It Solve?

Police departments have limited mobile patrol units that cannot cover every location at the same time.

The challenge is to determine:

* Which areas should receive patrol coverage?
* How can patrol units be distributed across high-risk areas?
* How can excessive concentration of patrol units be avoided?
* Which patrol unit should respond to an emergency?
* What road route should be taken to reach the location?

Q-Patrol combines optimization and GIS-based routing to create a single interactive platform for exploring these problems.

---

## How Q-Patrol Works

The system follows this workflow:


City Risk Dataset
       ↓
Spatial Risk Analysis
       ↓
QUBO Patrol Optimization
       ↓
QAOA Quantum Simulation
       ↓
Patrol Location Selection
       ↓
OSRM Road Routing
       ↓
Emergency SOS Dispatch
       ↓
Incident Report


---

## Core Components

### 1. Spatial Risk Analysis

The system loads city-specific location and risk information.

Each location contains spatial coordinates and a risk score that can be used by the optimization model.

Example:


Location          Risk Score
--------------------------------
Devaraja             0.82
Mandi                0.91
Laxmipuram           0.71
Kuvempunagar         0.64
Metagalli            0.48


The data is visualized on an interactive map to provide a spatial view of the city.

---

### 2. QUBO Patrol Optimization

The patrol placement problem is represented as a **QUBO**.

QUBO stands for:

**Quadratic Unconstrained Binary Optimization**

Each location is represented using a binary variable:


xᵢ = 1 → Patrol assigned
xᵢ = 0 → No patrol


The QUBO considers:

* Risk associated with each location
* Proximity between patrol locations
* Required number of patrol units

The objective is to find patrol configurations with lower QUBO energy.

Conceptually:


High-risk location
        ↓
Higher patrol priority

Patrols too close
        ↓
Penalty

Wrong number of patrols
        ↓
Penalty


---

### 3. QAOA

QAOA stands for:

**Quantum Approximate Optimization Algorithm**

QAOA is used to explore possible solutions to the QUBO problem.

The QUBO is first converted into an **Ising Hamiltonian**, which is then represented using a Qiskit quantum circuit.

The circuit contains two important parameters:

### Gamma (γ)

Controls how strongly the quantum circuit follows the cost function.

### Beta (β)

Controls the mixing between different possible solutions.

The QAOA circuit produces a probability distribution over possible patrol configurations.

> **Current implementation:** QAOA is demonstrated using a 4-qubit Qiskit statevector simulation. It is not being executed on physical quantum hardware.

---

## 4. OSRM Road Routing

After patrol locations are determined, the system uses the **Open Source Routing Machine (OSRM)** to calculate routes using real road-network geometry.

Instead of using straight-line distance:


A ───────────────── B


the system follows available roads:


A
│
├──── Road ────┐
│              │
└──── Road ────┤
               B


The routing component can be used to calculate:

* Fastest road route
* Risk-weighted route
* Patrol-to-emergency route

---

## 5. Emergency SOS Dispatch

Q-Patrol includes an emergency dispatch workflow.

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


The selected patrol unit and route can then be displayed on the map.

---

## 6. Multi-City Support

The system supports city-specific datasets and dynamically updates the map and location information when the selected city changes.

Currently configured cities include:

* Bengaluru
* Mysuru
* Mangaluru
* Dharwad
* Hassan
* Hubballi
* Mandya
* Manipal
* Raichur
* Shivamogga
* Udupi

Each city contains its own location and spatial data.

---

## 7. Executive Incident Report

Q-Patrol can generate a structured `.txt` report containing information such as:

* Patrol assignments
* Risk information
* Spatial metrics
* Route information
* Emergency dispatch details

This provides a simple record that can be reviewed by a command-center user.




                        


---

# Technology Stack

| Component              | Technology          | Purpose                                  |
| ---------------------- | ------------------- | ---------------------------------------- |
| Frontend               | Streamlit           | Interactive command-center interface     |
| Mapping                | Folium / Leaflet.js | Interactive maps and route visualization |
| Routing                | OSRM API            | Real-world road routing                  |
| Quantum Computing      | Qiskit              | QAOA circuit construction and simulation |
| Optimization           | QUBO                | Patrol allocation model                  |
| Classical Optimization | SciPy MILP          | Classical optimization baseline          |
| Data Processing        | Pandas / NumPy      | Spatial and risk-data processing         |
| Graph Processing       | NetworkX            | Spatial graph and route calculations     |
| Language               | Python              | Core application development             |

---

# Quantum Optimization Model

The patrol allocation problem uses binary decision variables:


xᵢ ∈ {0, 1}


where:


1 → Patrol assigned
0 → No patrol


The QUBO combines three main considerations:

### Risk Reward

Higher-risk locations receive greater priority.

### Spatial Proximity

A penalty discourages excessive concentration of patrol units in nearby locations.

### Patrol Count

A penalty encourages the solution to use the required number of patrol units.

The resulting QUBO is converted into an Ising formulation and used to construct the QAOA circuit.

---

# Classical Baseline

The project also includes a classical **Mixed-Integer Linear Programming (MILP)** baseline using SciPy.

The classical solver provides a reference point for evaluating the optimization approach.

The project can compare aspects such as:

* Patrol allocation
* Execution time
* Problem size
* Optimization behavior

The QAOA component currently operates as a **4-qubit statevector simulation**, so the quantum results should be interpreted as a prototype demonstration rather than a comparison against physical quantum hardware.

---

# Project Structure


Q-Patrol/
│
├── app.py
├── quantum_solver.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── bengaluru.csv
│   ├── mysuru.csv
│   └── ...
│
└── assets/
    └── ...


