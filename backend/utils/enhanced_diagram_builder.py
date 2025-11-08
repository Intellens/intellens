import networkx as nx

def build_comprehensive_diagram(languages, services, connections):
    """Build diagram with languages and AWS services."""
    G = nx.DiGraph()
    
    # Add language nodes
    for lang, count in languages.items():
        G.add_node(f"lang_{lang}", 
                  type="language", 
                  label=f"{lang} ({count} files)",
                  category="Language")
    
    # Add service nodes
    for service, count in services.items():
        category = "Cloud Service" if any(x in service for x in ["AWS", "Azure", "GCP"]) else "Technology"
        G.add_node(f"service_{service.replace(' ', '_')}", 
                  type="service", 
                  label=f"{service} ({count} refs)",
                  category=category)
    
    # Add connections
    for src, dest in connections:
        if src and dest:
            G.add_edge(src, dest)
    
    # Build output
    nodes = []
    for node_id in G.nodes:
        node_data = G.nodes[node_id]
        nodes.append({
            "id": node_id,
            "label": node_data.get("label", node_id),
            "type": node_data.get("type", "unknown"),
            "category": node_data.get("category", "Other")
        })
    
    edges = [{"source": u, "target": v} for u, v in G.edges]
    
    return {
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "languages": languages,
            "services": services,
            "total_connections": len(edges)
        }
    }