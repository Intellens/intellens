# intellens

A project analysis tool that generates interactive architecture workflow diagrams from uploaded code projects.

## Features

- **Workflow Diagrams**: Generates step-by-step architecture workflows similar to AWS diagrams
- **Multi-language Support**: Analyzes Python, JavaScript, Terraform, and more
- **Service Detection**: Identifies cloud services, databases, and technologies
- **Interactive Visualization**: Web-based interface with workflow steps and components
- **Mermaid Export**: Generates Mermaid diagram syntax for documentation

## Quick Start

1. Start the backend: `cd backend && python3 -m uvicorn main:app --reload`
2. Open `frontend/index.html` in your browser
3. Upload a ZIP file containing your project
4. View the generated workflow diagram

## API Endpoints

- `POST /upload`: Upload project ZIP file and get analysis results including workflow diagram

## Workflow Diagram Output

The tool generates workflow diagrams with:
- Numbered steps showing the analysis process
- Technology components (languages, services)
- Project complexity assessment
- Mermaid diagram syntax for documentation
