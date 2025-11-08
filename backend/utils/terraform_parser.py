# -*- coding: utf-8 -*-
import os
import re
import json
from typing import Dict, List, Tuple, Any

class TerraformParser:
    """Parse Terraform files to extract AWS resources and their configurations."""
    
    def __init__(self):
        self.aws_service_mapping = {
            'aws_instance': {'type': 'compute', 'name': 'EC2', 'icon': '💻', 'category': 'Virtual Machine (VM)'},
            'aws_s3_bucket': {'type': 'storage', 'name': 'S3', 'icon': '🪣', 'category': 'Database'},
            'aws_dynamodb_table': {'type': 'database', 'name': 'DynamoDB', 'icon': '⚡', 'category': 'Database'},
            'aws_rds_instance': {'type': 'database', 'name': 'RDS', 'icon': '🗄️', 'category': 'Database'},
            'aws_lambda_function': {'type': 'compute', 'name': 'Lambda', 'icon': '🔶', 'category': 'Database'},
            'aws_cloudfront_distribution': {'type': 'cdn', 'name': 'CloudFront', 'icon': '🌐', 'category': 'Database'},
            'aws_route53_zone': {'type': 'dns', 'name': 'Route 53', 'icon': '🔄', 'category': 'Database'},
            'aws_api_gateway_rest_api': {'type': 'api', 'name': 'API Gateway', 'icon': '🔄', 'category': 'Database'},
            'aws_ecs_service': {'type': 'container', 'name': 'ECS', 'icon': '📦', 'category': 'Database'},
            'aws_eks_cluster': {'type': 'container', 'name': 'EKS', 'icon': '📦', 'category': 'Database'},
            'aws_vpc': {'type': 'network', 'name': 'VPC', 'icon': '🌐', 'category': 'Database'},
            'aws_security_group': {'type': 'security', 'name': 'Security Group', 'icon': '🔒', 'category': 'Security'},
            'aws_iam_role': {'type': 'security', 'name': 'IAM Role', 'icon': '🔐', 'category': 'Security'},
        }
    
    def parse_terraform_directory(self, directory_path: str) -> Dict[str, Any]:
        """Parse all Terraform files in a directory."""
        terraform_files = self._find_terraform_files(directory_path)
        
        all_resources = {}
        all_variables = {}
        all_outputs = {}
        
        for tf_file in terraform_files:
            try:
                content = self._read_file(tf_file)
                resources, variables, outputs = self._parse_terraform_content(content)
                
                # Merge results
                all_resources.update(resources)
                all_variables.update(variables)
                all_outputs.update(outputs)
                
            except Exception as e:
                print(f"Error parsing {tf_file}: {e}")
                continue
        
        return {
            'resources': all_resources,
            'variables': all_variables,
            'outputs': all_outputs,
            'diagram_data': self._generate_diagram_data(all_resources)
        }
    
    def _find_terraform_files(self, directory_path: str) -> List[str]:
        """Find all .tf files in the directory."""
        tf_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.tf'):
                    tf_files.append(os.path.join(root, file))
        return tf_files
    
    def _read_file(self, file_path: str) -> str:
        """Read file content."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_terraform_content(self, content: str) -> Tuple[Dict, Dict, Dict]:
        """Parse Terraform content to extract resources, variables, and outputs."""
        resources = {}
        variables = {}
        outputs = {}
        
        # Remove comments
        content = re.sub(r'#.*', '', content)
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Parse resource blocks
        resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        for match in re.finditer(resource_pattern, content, re.DOTALL):
            resource_type = match.group(1)
            resource_name = match.group(2)
            resource_config = match.group(3)
            
            resources[f"{resource_type}.{resource_name}"] = {
                'type': resource_type,
                'name': resource_name,
                'config': self._parse_resource_config(resource_config)
            }
        
        # Parse variable blocks
        variable_pattern = r'variable\s+"([^"]+)"\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        for match in re.finditer(variable_pattern, content, re.DOTALL):
            var_name = match.group(1)
            var_config = match.group(2)
            variables[var_name] = self._parse_resource_config(var_config)
        
        # Parse output blocks
        output_pattern = r'output\s+"([^"]+)"\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        for match in re.finditer(output_pattern, content, re.DOTALL):
            output_name = match.group(1)
            output_config = match.group(2)
            outputs[output_name] = self._parse_resource_config(output_config)
        
        return resources, variables, outputs
    
    def _parse_resource_config(self, config_str: str) -> Dict[str, Any]:
        """Parse resource configuration block."""
        config = {}
        
        # Simple key-value pairs
        kv_pattern = r'(\w+)\s*=\s*"([^"]*)"'
        for match in re.finditer(kv_pattern, config_str):
            key = match.group(1)
            value = match.group(2)
            config[key] = value
        
        # Boolean values
        bool_pattern = r'(\w+)\s*=\s*(true|false)'
        for match in re.finditer(bool_pattern, config_str):
            key = match.group(1)
            value = match.group(2) == 'true'
            config[key] = value
        
        # Numeric values
        num_pattern = r'(\w+)\s*=\s*(\d+(?:\.\d+)?)'
        for match in re.finditer(num_pattern, config_str):
            key = match.group(1)
            value = match.group(2)
            config[key] = float(value) if '.' in value else int(value)
        
        # Tags block
        tags_pattern = r'tags\s*=\s*\{([^{}]*)\}'
        tags_match = re.search(tags_pattern, config_str)
        if tags_match:
            tags_content = tags_match.group(1)
            tags = {}
            for match in re.finditer(kv_pattern, tags_content):
                tags[match.group(1)] = match.group(2)
            config['tags'] = tags
        
        return config
    
    def _generate_diagram_data(self, resources: Dict[str, Any]) -> Dict[str, Any]:
        """Generate diagram data from parsed resources."""
        services = []
        groups = {'Virtual Machine (VM)': [], 'Database': [], 'Security': []}
        
        for resource_id, resource_data in resources.items():
            resource_type = resource_data['type']
            
            if resource_type in self.aws_service_mapping:
                service_info = self.aws_service_mapping[resource_type]
                
                service = {
                    'id': resource_id,
                    'type': resource_type,
                    'name': service_info['name'],
                    'icon': service_info['icon'],
                    'category': service_info['category'],
                    'resource_name': resource_data['name'],
                    'config': resource_data['config'],
                    'description': self._get_service_description(resource_type, resource_data['config'])
                }
                
                services.append(service)
                
                # Group services by category
                category = service_info['category']
                if category in groups:
                    groups[category].append(service)
        
        return {
            'services': services,
            'groups': groups,
            'total_services': len(services)
        }
    
    def _get_service_description(self, resource_type: str, config: Dict[str, Any]) -> str:
        """Generate service description based on configuration."""
        descriptions = {
            'aws_instance': f"EC2 instance ({config.get('instance_type', 'unknown type')})",
            'aws_s3_bucket': f"S3 bucket for storage",
            'aws_dynamodb_table': f"DynamoDB table ({config.get('billing_mode', 'unknown billing')})",
            'aws_rds_instance': f"RDS database ({config.get('engine', 'unknown engine')})",
            'aws_lambda_function': f"Lambda function ({config.get('runtime', 'unknown runtime')})",
            'aws_cloudfront_distribution': "CloudFront CDN distribution",
            'aws_route53_zone': "Route 53 DNS zone",
            'aws_api_gateway_rest_api': "API Gateway REST API",
            'aws_ecs_service': "ECS container service",
            'aws_eks_cluster': "EKS Kubernetes cluster",
            'aws_vpc': "Virtual Private Cloud",
            'aws_security_group': "Security group for network access",
            'aws_iam_role': "IAM role for permissions"
        }
        
        return descriptions.get(resource_type, f"{resource_type} resource")