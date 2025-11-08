# Infrastructure Diagram

```mermaid
flowchart LR
    User([👤 User]) 
    
%{ for type, instances in resources ~}
%{ for name, config in instances ~}
%{ if type == "s3" ~}
    ${type}_${name}[🗄️ S3 Bucket<br/>${name}]
%{ endif ~}
%{ if type == "ec2" ~}
    ${type}_${name}[🖥️ EC2 Instance<br/>${name}]
%{ endif ~}
%{ if type == "lambda" ~}
    ${type}_${name}[⚡ Lambda Function<br/>${name}]
%{ endif ~}
%{ if type == "rds" ~}
    ${type}_${name}[🗃️ RDS Database<br/>${name}]
%{ endif ~}
%{ endfor ~}
%{ endfor ~}

    Interface[🌐 Web Interface]
    API[🔗 API Gateway]
    
    User --> Interface
    Interface --> API
    
%{ if try(length(resources.ec2), 0) > 0 ~}
%{ for ec2_name, ec2_config in resources.ec2 ~}
    API --> ec2_${ec2_name}
%{ endfor ~}
%{ endif ~}

%{ if try(length(resources.lambda), 0) > 0 ~}
%{ for lambda_name, lambda_config in resources.lambda ~}
    API --> lambda_${lambda_name}
%{ endfor ~}
%{ endif ~}

%{ if try(length(resources.ec2), 0) > 0 && try(length(resources.s3), 0) > 0 ~}
%{ for ec2_name, ec2_config in resources.ec2 ~}
%{ for s3_name, s3_config in resources.s3 ~}
    ec2_${ec2_name} --> s3_${s3_name}
%{ endfor ~}
%{ endfor ~}
%{ endif ~}

%{ if try(length(resources.lambda), 0) > 0 && try(length(resources.s3), 0) > 0 ~}
%{ for lambda_name, lambda_config in resources.lambda ~}
%{ for s3_name, s3_config in resources.s3 ~}
    lambda_${lambda_name} --> s3_${s3_name}
%{ endfor ~}
%{ endfor ~}
%{ endif ~}

%{ if try(length(resources.ec2), 0) > 0 && try(length(resources.rds), 0) > 0 ~}
%{ for ec2_name, ec2_config in resources.ec2 ~}
%{ for rds_name, rds_config in resources.rds ~}
    ec2_${ec2_name} --> rds_${rds_name}
%{ endfor ~}
%{ endfor ~}
%{ endif ~}

    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef user fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef interface fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    
    class User user
    class Interface,API interface
%{ for type, instances in resources ~}
%{ for name, config in instances ~}
    class ${type}_${name} aws
%{ endfor ~}
%{ endfor ~}
```