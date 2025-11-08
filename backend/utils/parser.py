import os
import hcl2

def parse_terraform_files(folder_path):
    """Parse Terraform files and return services + connections."""
    services = set()
    connections = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".tf"):
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    try:
                        data = hcl2.load(f)
                    except Exception:
                        continue

                    # Parse resources
                    if "resource" in data:
                        resource_data = data["resource"]
                        if isinstance(resource_data, list):
                            for item in resource_data:
                                if isinstance(item, dict):
                                    for resource_type in item.keys():
                                        services.add(resource_type)
                        elif isinstance(resource_data, dict):
                            for resource_type, items in resource_data.items():
                                for name, config in items.items():
                                    services.add(resource_type)
                                    if "depends_on" in config:
                                        for dep in config["depends_on"]:
                                            connections.append((dep, resource_type))

    return list(services), connections