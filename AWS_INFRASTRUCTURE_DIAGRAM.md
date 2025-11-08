# AWS Infrastructure Diagram Generator

This feature generates interactive AWS infrastructure diagrams from uploaded Terraform files, similar to the AWS Console designer interface.

## Features

### 🎯 Dynamic Analysis
- **Real Terraform Parsing**: Analyzes actual `.tf` files instead of hardcoded templates
- **Resource Detection**: Automatically identifies AWS resources (EC2, S3, DynamoDB, RDS, etc.)
- **Configuration Extraction**: Extracts resource configurations, tags, and relationships

### 🎨 Interactive Interface
- **AWS Console Style**: Three-panel layout similar to AWS Console designer
- **Service Sidebar**: Categorized AWS services with search functionality
- **Visual Canvas**: Grouped services with positioning and connections
- **Detail Panel**: Service configuration, Terraform code, and use cases

### 📊 Supported AWS Resources
- **Compute**: EC2, Lambda, ECS, EKS
- **Storage**: S3, EBS, EFS
- **Database**: DynamoDB, RDS, ElastiCache
- **Networking**: VPC, CloudFront, Route 53, API Gateway
- **Security**: IAM, Security Groups, WAF

## How It Works

### 1. File Upload
Upload a ZIP file containing Terraform (`.tf`) files.

### 2. Parsing Process
```python
# The system automatically:
1. Finds all .tf files in the uploaded project
2. Parses Terraform syntax to extract resources
3. Maps AWS resources to visual components
4. Groups services by category (VM, Database, Security)
5. Generates interactive diagram data
```

### 3. Diagram Generation
The system creates:
- **Sidebar**: AWS service categories for reference
- **Canvas**: Visual representation with grouped services
- **Panel**: Detailed configuration and Terraform code

## Example Output

For a Terraform file with:
```hcl
resource "aws_instance" "web_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name = "web-server"
    Environment = "production"
  }
}

resource "aws_s3_bucket" "static_assets" {
  bucket = "demo-app-static-assets"
  
  tags = {
    Name = "static-assets"
    Environment = "production"
  }
}
```

The system generates:
- **EC2 service** in the "Virtual Machine (VM)" group
- **S3 service** in the "Database" group  
- **Interactive connections** between related services
- **Configuration details** with Terraform code snippets

## Interface Components

### Left Sidebar
- **Search Bar**: Filter AWS services
- **Service Categories**: Compute, Storage, Database, Networking, Security
- **Service Icons**: Visual representation of each AWS service

### Center Canvas
- **Service Groups**: VM, Database, Security sections
- **Service Cards**: Individual AWS resources with icons and names
- **Connections**: Visual links between related services
- **Interactive Selection**: Click services to view details

### Right Panel
- **Service Details**: Name, description, and configuration
- **Terraform Code**: Generated HCL syntax
- **Use Cases**: Common applications for the service
- **Configuration Values**: Resource-specific settings

## Technical Implementation

### Backend Components
- `terraform_parser.py`: Parses .tf files and extracts resources
- `aws_diagram_generator.py`: Creates diagram data structure
- Enhanced API endpoint returns `aws_infrastructure_diagram`

### Frontend Components
- `aws-infrastructure-designer.js`: Interactive diagram renderer
- CSS styling for AWS Console-like appearance
- Event handlers for service selection and filtering

## Usage

1. **Start the backend**: `cd backend && python3 -m uvicorn main:app --reload`
2. **Open frontend**: Open `frontend/index.html` in browser
3. **Upload project**: Select ZIP file with Terraform files
4. **View diagram**: Interactive AWS infrastructure diagram appears in "Terraform Infrastructure" section

## Benefits

- **Visual Understanding**: See your infrastructure at a glance
- **Interactive Exploration**: Click services to see configurations
- **Code Generation**: View corresponding Terraform syntax
- **Architecture Planning**: Understand service relationships
- **Documentation**: Export diagrams for documentation

## Example Projects

The system works with any Terraform project containing AWS resources:
- Web applications with EC2 + RDS
- Serverless architectures with Lambda + DynamoDB
- Static websites with S3 + CloudFront
- Microservices with ECS + API Gateway

Upload your Terraform project and see your infrastructure come to life! 🚀