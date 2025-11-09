import boto3
import json
import os
from typing import Dict, List

class ProjectSummaryGenerator:
    """Generate AI-powered project summaries using AWS Bedrock."""
    
    def __init__(self):
        try:
            self.client = boto3.client('bedrock-runtime', region_name='us-east-1')
        except:
            self.client = None
    
    def generate_project_summary(self, languages: Dict, services: Dict, project_name: str, file_details: List) -> str:
        """Generate a comprehensive project summary using Bedrock."""
        if not self.client:
            return self._get_fallback_summary(languages, services, project_name)
        
        try:
            # Prepare context for the AI
            lang_list = list(languages.keys())
            service_list = list(services.keys())
            total_files = sum(languages.values())
            
            prompt = f"""
            Generate a comprehensive project summary for a software project with the following details:
            
            Project Name: {project_name}
            Programming Languages: {', '.join(lang_list)} (Total files: {total_files})
            Technologies/Services: {', '.join(service_list[:10])}
            
            Write a 2-3 paragraph summary that:
            1. Describes what this project is and its purpose
            2. Highlights the key technologies and their roles
            3. Assesses the project's complexity and architecture approach
            
            Keep it professional, concise, and insightful. Focus on the technical architecture and business value. Be direct and confident in your assessment.
            """
            
            response = self.client.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            return result['content'][0]['text'].strip()
            
        except Exception as e:
            print(f"Bedrock error generating project summary: {e}")
            return self._get_fallback_summary(languages, services, project_name)
    
    def _get_fallback_summary(self, languages: Dict, services: Dict, project_name: str) -> str:
        """Fallback summary when Bedrock is unavailable."""
        lang_list = list(languages.keys())
        service_list = list(services.keys())
        total_files = sum(languages.values())
        
        complexity = "high" if len(services) > 5 else "medium" if len(services) > 2 else "moderate"
        
        summary = f"""This project is a {complexity}-complexity software application built with {', '.join(lang_list[:3])}. """
        
        if len(lang_list) > 1:
            summary += f"The multi-language architecture suggests a modular approach, leveraging the strengths of each technology stack. "
        
        if service_list:
            summary += f"The project integrates with {len(service_list)} external services including {', '.join(service_list[:3])}, indicating a cloud-native or service-oriented architecture. "
        
        summary += f"With {total_files} source files across {len(lang_list)} programming languages, this represents a substantial codebase designed for scalability and maintainability."
        
        return summary