#!/usr/bin/env python3
"""
Demo script showing the enhanced layered architecture with Gemini-like intelligence
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.terraform_diagram_generator import generate_terraform_diagram, generate_terraform_hcl
import json

def demo_complex_architecture():
    """Demo a complex multi-tier architecture"""
    
    print("🏗️  Enhanced Architecture Generator Demo")
    print("=" * 60)
    
    # Simulate a complex e-commerce application
    languages = {
        'Python': 12,      # Backend APIs
        'JavaScript': 8,   # Frontend
        'TypeScript': 5,   # React components
        'SQL': 4,          # Database queries
        'YAML': 3,         # Kubernetes configs
        'Dockerfile': 2    # Container configs
    }
    
    services = {
        'api': True,           # REST APIs
        'auth': True,          # User authentication
        'serverless': True,    # Lambda functions
        'container': True,     # ECS/Docker
        'nosql_database': True, # DynamoDB
        'sql_database': True,  # RDS PostgreSQL
        'storage': True,       # S3 buckets
        'cdn': True,          # CloudFront
        'dns': True           # Route 53
    }
    
    project_name = "ECommerceApp"
    
    print(f"📊 Analyzing {project_name}...")
    print(f"Languages detected: {list(languages.keys())}")
    print(f"Services detected: {list(services.keys())}")
    print()
    
    # Generate the enhanced architecture
    result = generate_terraform_diagram(languages, services, project_name)
    diagram = result['diagram']
    
    print("🎯 Generated Layered Architecture")
    print("-" * 40)
    print(f"Style: {diagram['style']}")
    print(f"Total Services: {len(diagram['services'])}")
    print(f"Total Connections: {len(diagram['connections'])}")
    print()
    
    # Show processing order
    print("📋 Processing Order & Layers")
    print("-" * 40)
    for layer_name, layer_info in diagram['processing_order']:
        if layer_info['services']:
            print(f"\n{layer_info['order']}. {layer_info['name']}")
            print(f"   📝 {layer_info['description']}")
            for service in layer_info['services']:
                print(f"   {service['icon']} {service['name']} ({service['category']})")
    
    print("\n🔗 Service Connections")
    print("-" * 40)
    for conn in diagram['connections']:
        print(f"{conn['source']} --[{conn['type']}]--> {conn['target']}")
        print(f"   💬 {conn['description']}")
    
    print("\n⚡ Processing Workflow")
    print("-" * 40)
    for step in diagram['workflow_steps']:
        print(f"\nStep {step['step']}: {step['title']}")
        print(f"📋 {step['description']}")
        print(f"🔧 Services: {', '.join(step['services'])}")
        print(f"💡 Details: {step['processing_details']}")
    
    # Generate Terraform code
    terraform_hcl = generate_terraform_hcl(result['terraform_config'])
    
    print("\n🏗️  Generated Terraform Configuration")
    print("-" * 40)
    print(terraform_hcl[:500] + "..." if len(terraform_hcl) > 500 else terraform_hcl)
    
    # Save detailed output
    output_file = f"{project_name.lower()}_architecture.json"
    with open(output_file, 'w') as f:
        json.dump({
            'diagram': diagram,
            'terraform_config': result['terraform_config'],
            'terraform_hcl': terraform_hcl
        }, f, indent=2)
    
    print(f"\n💾 Full architecture saved to: {output_file}")
    
    # Show architecture insights
    print("\n🧠 Architecture Insights (Gemini-like Analysis)")
    print("-" * 50)
    
    insights = analyze_architecture_patterns(diagram)
    for insight in insights:
        print(f"• {insight}")
    
    return result

def analyze_architecture_patterns(diagram):
    """Analyze architecture patterns like Gemini would"""
    insights = []
    
    # Analyze layer distribution
    layer_counts = {}
    for service in diagram['services']:
        layer = service['layer']
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    
    if layer_counts.get('presentation', 0) > 0 and layer_counts.get('data', 0) > 0:
        insights.append("✅ Well-structured multi-tier architecture detected")
    
    if layer_counts.get('application', 0) >= 2:
        insights.append("🔄 Microservices pattern identified with multiple application components")
    
    # Analyze connections
    connection_types = [conn['type'] for conn in diagram['connections']]
    if 'read/write' in connection_types:
        insights.append("💾 Direct database access pattern detected")
    
    if 'invoke' in connection_types:
        insights.append("⚡ Serverless invocation pattern identified")
    
    # Check for best practices
    service_ids = [s['id'] for s in diagram['services']]
    if 'cdn' in service_ids and 's3' in service_ids:
        insights.append("🌐 Optimal content delivery setup with CDN + S3")
    
    if 'auth' in service_ids:
        insights.append("🔐 Security-first approach with dedicated authentication")
    
    if len(diagram['services']) >= 5:
        insights.append("🏢 Enterprise-grade architecture with comprehensive service coverage")
    
    return insights

if __name__ == "__main__":
    demo_complex_architecture()