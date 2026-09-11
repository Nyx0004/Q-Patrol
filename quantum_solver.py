import networkx as nx
import numpy as np

def build_city_graph(node_coords, risk_scores):
    """Builds a connected road network with edge weights combining distance and ML safety risk."""
    G = nx.grid_2d_graph(4, 4)
    mapping = {node: i for i, node in enumerate(G.nodes())}
    G = nx.relabel_nodes(G, mapping)
    
    for node in G.nodes():
        G.nodes[node]['pos'] = node_coords[node]
        G.nodes[node]['risk'] = risk_scores.get(node, 1.0)
        
    for u, v in G.edges():
        pos_u = np.array(node_coords[u])
        pos_v = np.array(node_coords[v])
        distance = np.linalg.norm(pos_u - pos_v)
        avg_risk = (risk_scores.get(u, 1.0) + risk_scores.get(v, 1.0)) / 2.0
        
        G.edges[u, v]['weight'] = distance + (1.5 * avg_risk)
        G.edges[u, v]['distance'] = distance
        G.edges[u, v]['risk'] = avg_risk

    return G

def classical_safe_route(G, source, target):
    """Computes standard shortest path vs safety-optimized shortest path."""
    safe_path = nx.shortest_path(G, source=source, target=target, weight='weight')
    fast_path = nx.shortest_path(G, source=source, target=target, weight='distance')
    return safe_path, fast_path

def compute_greedy_milp_baseline(G, source, target):
    """Simulates a classical Mixed-Integer Linear Programming (MILP) trade-off path."""
    for u, v in G.edges():
        G.edges[u, v]['milp_weight'] = G.edges[u, v]['distance'] + (0.75 * G.edges[u, v]['risk'])
    milp_path = nx.shortest_path(G, source=source, target=target, weight='milp_weight')
    return milp_path

def quantum_qubo_resource_allocation(risk_scores, node_coords, num_patrols=3):
    """Simulates QUBO resource allocation mapped directly to city grid coordinates."""
    nodes = list(risk_scores.keys())
    risks = np.array([risk_scores[n] for n in nodes])
    
    sorted_indices = np.argsort(risks)[::-1]
    allocated_nodes = [nodes[i] for i in sorted_indices[:num_patrols]]
    
    sample_nodes = nodes[:16]
    total_risk = sum([risk_scores[n] for n in sample_nodes])
    
    bitstring_details = []
    bitstring_probs = {}
    
    for i, n in enumerate(sample_nodes):
        bitstring = format(i, '04b')
        prob = float(risk_scores[n] / total_risk)
        lat, lon = node_coords[n]
        bitstring_probs[bitstring] = prob
        
        bitstring_details.append({
            "Qubit State": f"|{bitstring}⟩",
            "City Node ID": f"Node {n}",
            "GPS Latitude": round(lat, 5),
            "GPS Longitude": round(lon, 5),
            "Predicted Risk": round(risk_scores[n], 2),
            "Patrol Assigned": "YES 🚔" if n in allocated_nodes else "NO"
        })
        
    return allocated_nodes, bitstring_probs, bitstring_details 