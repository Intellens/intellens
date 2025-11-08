# Demo Terraform configuration for diagram generation
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Mock infrastructure data
locals {
  resources = {
    ec2 = {
      web_server = {
        instance_type = "t2.micro"
        ami = "ami-0c02fb55956c7d316"
      }
    }
    s3 = {
      app_bucket = {
        bucket = "my-app-bucket"
      }
    }
    lambda = {
      processor = {
        runtime = "python3.9"
        handler = "index.handler"
      }
    }
  }
  
  mermaid_diagram = templatefile("${path.module}/templates/mermaid.tpl", {
    resources = local.resources
  })
}

# Output diagram
output "infrastructure_diagram" {
  value = local.mermaid_diagram
}

# Generate diagram file
resource "local_file" "diagram_output" {
  content  = local.mermaid_diagram
  filename = "${path.module}/infrastructure-diagram.md"
}