#!/usr/bin/env python3
"""
Test script for the enhanced layered architecture diagram generator
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.terraform_diagram_generator import generate_terraform_diagram
import json

def test_layered_architecture():
    """Test the layered architecture generation"""
    
    # Mock detected services (simulating a typical web application)
    test_languages = {
        'Python': 5,
        'JavaScript': 3,
        'SQL': 2
    }
    
    test_services = {
        'api': True,
        'serverless': True,
        'nosql_database': True,
        'storage': True,
        'cdn': True,
        'auth': True
    }
    
    print("Testing Layered Architecture Generation...")
    print("=" * 50)
    
    # Generate the diagram
    result = generate_terraform_diagram(test_languages, test_services, "TestWebApp")
    
    print(f"Generated diagram style: {result['diagram']['style']}")
    print(f"Project name: {result['diagram']['project_name']}")
    print(f"Total services: {len(result['diagram']['services'])}")
    print(f"Total connections: {len(result['diagram']['connections'])}")
    
    print("\nServices:")
    print("-" * 30)
    for service in result['diagram']['services']:
        print(f"• {service['name']} ({service['category']}) - {service['id']}")
    
    print("\nConnections:")
    print("-" * 30)
    for conn in result['diagram']['connections']:
        print(f"{conn['source']} -> {conn['target']} ({conn['type']})")
    
    print("\nWorkflow Steps:")
    print("-" * 30)
    for step in result['diagram']['workflow_steps']:
        print(f"Step {step['step']}: {step['service']} - {step['description']}")
    
    print("\nTerraform Configuration Preview:")
    print("-" * 30)
    print(f"Provider: {result['terraform_config']['provider']}")
    print(f"Resources: {len(result['terraform_config']['resource'])} defined")
    
    return result

if __name__ == "__main__":
    test_result = test_layered_architecture()
    
    # Save result for inspection
    with open('test_layered_output.json', 'w') as f:
        json.dump(test_result, f, indent=2)
    
    print(f"\nTest completed! Enhanced diagram with connections generated.")
    print(f"Full output saved to test_layered_output.json")