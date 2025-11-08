#!/usr/bin/env python3
"""Test script for Terraform parser and AWS diagram generator."""

import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.terraform_parser import TerraformParser
from utils.aws_diagram_generator import AWSInfrastructureDiagramGenerator

def test_terraform_parser():
    """Test the Terraform parser with sample files."""
    print("Testing Terraform Parser...")
    
    parser = TerraformParser()
    terraform_dir = os.path.join(os.path.dirname(__file__), 'terraform')
    
    try:
        result = parser.parse_terraform_directory(terraform_dir)
        
        print(f"Found {len(result['resources'])} resources:")
        for resource_id, resource_data in result['resources'].items():
            print(f"  - {resource_id}: {resource_data['type']}")
        
        print(f"\nDiagram data:")
        print(f"  - Total services: {result['diagram_data']['total_services']}")
        print(f"  - Service groups: {list(result['diagram_data']['groups'].keys())}")
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_aws_diagram_generator():
    """Test the AWS diagram generator."""
    print("\nTesting AWS Diagram Generator...")
    
    generator = AWSInfrastructureDiagramGenerator()
    terraform_dir = os.path.join(os.path.dirname(__file__), 'terraform')
    
    try:
        diagram_data = generator.generate_infrastructure_diagram(terraform_dir, "Test Project")
        
        print(f"Generated diagram for: {diagram_data['project_name']}")
        print(f"Canvas groups: {len(diagram_data['canvas']['groups'])}")
        print(f"Total services: {diagram_data['summary']['total_services']}")
        print(f"Service types: {', '.join(diagram_data['summary']['service_types'])}")
        
        # Print sample service details
        if diagram_data['canvas']['services']:
            sample_service = diagram_data['canvas']['services'][0]
            print(f"\nSample service: {sample_service['name']} ({sample_service['resource_name']})")
        
        return diagram_data
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Run tests."""
    print("=" * 50)
    print("Terraform Infrastructure Analyzer Test")
    print("=" * 50)
    
    # Test parser
    parser_result = test_terraform_parser()
    
    # Test diagram generator
    diagram_result = test_aws_diagram_generator()
    
    if parser_result and diagram_result:
        print("\n✅ All tests passed!")
        
        # Save sample output
        output_file = "sample_diagram_output.json"
        with open(output_file, 'w') as f:
            json.dump(diagram_result, f, indent=2, default=str)
        print(f"📄 Sample output saved to: {output_file}")
        
    else:
        print("\n❌ Some tests failed!")

if __name__ == "__main__":
    main()