import os
import boto3
import json
from typing import Dict, List

class DescriptionGenerator:
    """Generate descriptions for programming languages and services using Bedrock."""
    
    def __init__(self):
        # Configure Bedrock
        try:
            self.client = boto3.client('bedrock-runtime', region_name='us-east-1')
        except:
            self.client = None
    
    def get_language_description(self, language: str, file_count: int) -> Dict[str, any]:
        """Get comprehensive description for a programming language."""
        if not self.client:
            return self._get_fallback_language_description(language, file_count)
        
        try:
            prompt = f"""
            Provide a comprehensive description for the programming language: {language}
            
            Format your response as JSON with these exact keys:
            {{
                "description": "Brief 2-3 sentence description of what {language} is and its main purpose",
                "use_cases": ["use case 1", "use case 2", "use case 3", "use case 4"],
                "characteristics": ["key feature 1", "key feature 2", "key feature 3"],
                "configuration": {{"key1": "value1", "key2": "value2"}},
                "resource_name": "suggested-resource-name",
                "terraform_config": "Complete terraform resource block for {language} deployment"
            }}
            
            Keep descriptions concise and practical. Focus on real-world applications.
            """
            
            response = self.client.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            response_text = result['content'][0]['text']
            
            # Parse JSON response
            try:
                result = json.loads(response_text.strip())
                return {
                    'description': result['description'],
                    'use_cases': result['use_cases'],
                    'characteristics': result['characteristics'],
                    'configuration': result.get('configuration', {}),
                    'resource_name': result.get('resource_name', f'{language.lower()}-app'),
                    'terraform_config': result.get('terraform_config', f'# {language} application configuration')
                }
            except (json.JSONDecodeError, KeyError):
                return self._get_fallback_language_description(language, file_count)
            
        except Exception as e:
            print(f"Bedrock error for {language}: {e}")
            return self._get_fallback_language_description(language, file_count)
    
    def get_service_description(self, service: str, reference_count: int) -> Dict[str, any]:
        """Get comprehensive description for a service or technology."""
        if not self.client:
            return self._get_fallback_service_description(service, reference_count)
        
        try:
            prompt = f"""
            Provide a comprehensive description for the technology/service: {service}
            
            Format your response as JSON with these exact keys:
            {{
                "description": "Brief 2-3 sentence description of what {service} is and its main purpose",
                "use_cases": ["use case 1", "use case 2", "use case 3", "use case 4"],
                "integration_benefits": ["benefit 1", "benefit 2", "benefit 3"],
                "configuration": {{"key1": "value1", "key2": "value2"}},
                "resource_name": "suggested-resource-name",
                "terraform_config": "Complete terraform resource block for {service} deployment"
            }}
            
            Keep descriptions concise and practical. Focus on real-world applications and integration benefits.
            """
            
            response = self.client.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            response_text = result['content'][0]['text']
            
            # Parse JSON response
            try:
                result = json.loads(response_text.strip())
                return {
                    'description': result['description'],
                    'use_cases': result['use_cases'],
                    'integration_benefits': result['integration_benefits'],
                    'configuration': result.get('configuration', {}),
                    'resource_name': result.get('resource_name', service.lower().replace(' ', '-')),
                    'terraform_config': result.get('terraform_config', f'# {service} configuration')
                }
            except (json.JSONDecodeError, KeyError):
                return self._get_fallback_service_description(service, reference_count)
            
        except Exception as e:
            print(f"Bedrock error for {service}: {e}")
            return self._get_fallback_service_description(service, reference_count)
    
    def _get_fallback_language_description(self, language: str, file_count: int) -> Dict[str, any]:
        """Fallback descriptions when Bedrock is unavailable."""
        fallbacks = {
            'Python': {
                'description': 'Python is a high-level, interpreted programming language known for its simplicity and readability. It\'s widely used for web development, data science, automation, and artificial intelligence applications.',
                'use_cases': ['Web development with Django/Flask', 'Data science and machine learning', 'Automation and scripting', 'API development'],
                'characteristics': ['Easy to learn and read', 'Extensive library ecosystem', 'Cross-platform compatibility']
            },
            'JavaScript': {
                'description': 'JavaScript is a dynamic programming language primarily used for web development. It enables interactive web pages and is essential for front-end development, with growing use in back-end development through Node.js.',
                'use_cases': ['Frontend web development', 'Backend development with Node.js', 'Mobile app development', 'Desktop applications'],
                'characteristics': ['Dynamic and flexible', 'Event-driven programming', 'Large ecosystem of frameworks']
            }
        }
        
        return fallbacks.get(language, {
            'description': f'{language} is a programming language used in this project.',
            'use_cases': ['Software development', 'Application building', 'Problem solving', 'System implementation'],
            'characteristics': ['Programming language', 'Used in software development', 'Part of this project'],
            'configuration': {'type': language.lower(), 'files': file_count},
            'resource_name': f'{language.lower()}-app',
            'terraform_config': f'# {language} application\nresource "aws_instance" "{language.lower()}-app" {{\n  ami = "ami-12345678"\n  instance_type = "t3.micro"\n}}'
        })
    
    def _get_fallback_service_description(self, service: str, reference_count: int) -> Dict[str, any]:
        """Fallback descriptions for services when Bedrock is unavailable."""
        fallbacks = {
            'React': {
                'description': 'React is a JavaScript library for building user interfaces with a component-based architecture. It enables developers to create interactive and dynamic web applications efficiently.',
                'use_cases': ['Single-page applications', 'Interactive web interfaces', 'Component-based UI development', 'Progressive web apps'],
                'integration_benefits': ['Reusable components', 'Virtual DOM performance', 'Large ecosystem']
            }
        }
        
        return fallbacks.get(service, {
            'description': f'{service} is a technology or service integrated into this project.',
            'use_cases': ['System integration', 'Application enhancement', 'Service provision', 'Technology implementation'],
            'integration_benefits': ['Enhanced functionality', 'Improved capabilities', 'System integration'],
            'configuration': {'type': service.lower().replace(' ', '_'), 'references': reference_count},
            'resource_name': service.lower().replace(' ', '-'),
            'terraform_config': f'# {service} configuration\nresource "null_resource" "{service.lower().replace(" ", "_")}" {{\n  # Configuration for {service}\n}}'
        })