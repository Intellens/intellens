import json
import networkx as nx

# Simple AWS service descriptions
SERVICE_INFO = {
    "aws_s3_bucket": "Amazon S3 provides object storage for data and media.",
    "aws_instance": "Amazon EC2 is a compute service for running virtual servers.",
    "aws_lambda_function": "AWS Lambda runs code in response to events without managing servers.",
}

def build_graph_json(services, connections):
    """Create a graph of services and connections."""
    G = nx.DiGraph()

    # Add nodes
    for s in services:
        G.add_node(s, label=s, description=SERVICE_INFO.get(s, "Service info not available."))

    # Add connections
    for src, dest in connections:
        G.add_edge(src, dest)

    # Build JSON output
    nodes = [
        {"id": n, "label": G.nodes[n]["label"], "description": G.nodes[n]["description"]}
        for n in G.nodes
    ]
    edges = [{"source": u, "target": v} for u, v in G.edges]

    return {"nodes": nodes, "edges": edges}