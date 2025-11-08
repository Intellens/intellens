# Terraform Diagram Generator

Generates infrastructure diagrams directly from Terraform configuration.

## Usage

1. Include the diagram module in your Terraform configuration:

```hcl
module "diagram" {
  source = "./diagram"
  
  ec2_instances = {
    web_server = aws_instance.web_server
  }
  
  s3_buckets = {
    app_bucket = aws_s3_bucket.app_bucket
  }
}
```

2. Run Terraform:

```bash
terraform init
terraform plan
terraform apply
```

3. View the generated diagram:

```bash
terraform output infrastructure_diagram
```

The diagram will also be saved to `infrastructure-diagram.md`.

## Features

- Generates Mermaid diagrams
- Outputs as Terraform output values
- Creates markdown files with diagrams
- Supports EC2, S3, Lambda, RDS resources
- Automatic relationship detection