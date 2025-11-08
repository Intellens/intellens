import re
from collections import defaultdict

def clean_service_name(service_name):
    """Clean and normalize service names to prevent concatenation."""
    # Remove common prefixes and suffixes
    service_name = service_name.strip()
    
    # Split on common delimiters and take the first meaningful part
    parts = service_name.replace('_', ' ').replace('-', ' ').split()
    if len(parts) > 3:  # If too many parts, likely concatenated
        # Take first 2-3 meaningful parts
        meaningful_parts = []
        for part in parts[:3]:
            if len(part) > 2 and part.lower() not in ['aws', 'amazon', 'service']:
                meaningful_parts.append(part)
        if meaningful_parts:
            return ' '.join(meaningful_parts[:2])
    
    # Limit length to prevent extremely long names
    if len(service_name) > 30:
        return service_name[:30] + '...'
    
    return service_name

def auto_detect_services(content):
    """Automatically detect cloud services and technologies from content."""
    services = defaultdict(int)
    
    # AWS service patterns with clean names
    aws_service_map = {
        'lambda': 'AWS Lambda',
        's3': 'AWS S3',
        'ec2': 'AWS EC2',
        'rds': 'AWS RDS',
        'dynamodb': 'AWS DynamoDB',
        'iot': 'AWS IoT Core',
        'kinesis': 'AWS Kinesis',
        'firehose': 'AWS Kinesis Data Firehose',
        'greengrass': 'AWS IoT Greengrass',
        'lex': 'Amazon Lex',
        'sqs': 'AWS SQS',
        'sns': 'AWS SNS',
        'cloudformation': 'AWS CloudFormation',
        'cloudwatch': 'AWS CloudWatch'
    }
    
    # More precise AWS service detection
    aws_patterns = [
        r'aws[_-]([a-zA-Z0-9]+)',
        r'amazonaws\.com/([a-zA-Z0-9-]+)',
        r'\b(lambda|s3|ec2|rds|dynamodb|iot|kinesis|firehose|greengrass|lex|sqs|sns|cloudformation|cloudwatch|apigateway|cognito|amplify)\b',
        r'@aws-sdk/([a-zA-Z0-9-]+)',
        r'boto3\.',
        r'aws\s+([a-zA-Z0-9]+)',
        r'AWS::([a-zA-Z0-9:]+)'
    ]
    
    for pattern in aws_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0] if match[0] else match[1]
            clean_name = aws_service_map.get(match.lower(), f'AWS {match.capitalize()}')
            clean_name = clean_service_name(clean_name)
            services[clean_name] += 1
    
    # Generic cloud patterns with clean names
    cloud_patterns = {
        r'\.s3\.': 'AWS S3',
        r'\.ec2\.': 'AWS EC2', 
        r'\.lambda\.': 'AWS Lambda',
        r'\.rds\.': 'AWS RDS',
        r'\.dynamodb\.': 'AWS DynamoDB',
        r'azure\.': 'Microsoft Azure',
        r'gcp\.': 'Google Cloud Platform',
        r'kubernetes': 'Kubernetes',
        r'docker': 'Docker',
        r'redis': 'Redis',
        r'mongodb': 'MongoDB',
        r'postgresql': 'PostgreSQL',
        r'mysql': 'MySQL',
        r'nginx': 'Nginx',
        r'apache': 'Apache',
        r'terraform': 'Terraform',
        r'express': 'Express.js',
        r'fastapi': 'FastAPI',
        r'django': 'Django',
        r'flask': 'Flask',
        r'react': 'React',
        r'vue': 'Vue.js',
        r'angular': 'Angular'
    }
    
    for pattern, service in cloud_patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            clean_name = clean_service_name(service)
            services[clean_name] += 1
    
    # Extract from imports/requires
    import_patterns = [
        r'import\s+([a-zA-Z0-9_-]+)',
        r'from\s+([a-zA-Z0-9_.-]+)',
        r'require\([\'"]([a-zA-Z0-9_.-]+)[\'"]',
        r'@([a-zA-Z0-9_-]+)/',  # npm packages
        r'pip\s+install\s+([a-zA-Z0-9_-]+)',
        r'npm\s+install\s+([a-zA-Z0-9_-]+)',
        r'yarn\s+add\s+([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if 'aws' in match.lower():
                clean_name = clean_service_name('AWS SDK')
                services[clean_name] += 1
            elif 'azure' in match.lower():
                clean_name = clean_service_name('Microsoft Azure')
                services[clean_name] += 1
            elif any(x in match.lower() for x in ['gcp', 'google-cloud']):
                clean_name = clean_service_name('Google Cloud Platform')
                services[clean_name] += 1
    
    return dict(services)

def detect_all_services(folder_path):
    """Scan all files and auto-detect services."""
    import os
    all_services = defaultdict(int)
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith('.'):
                continue
                
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    services = auto_detect_services(content)
                    for service, count in services.items():
                        all_services[service] += count
            except:
                continue
    
    return dict(all_services)