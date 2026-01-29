# Quantum Computing Risk Analyst for Banks

## Overview
A comprehensive Streamlit-based application for analyzing quantum computing threats to banking cryptographic infrastructure. The platform provides risk assessment, compliance checking, cost estimation, and migration planning capabilities.

## Project Structure
```
/
├── app.py                       # Main Streamlit dashboard application
├── modules/
│   ├── __init__.py             # Module initialization
│   ├── risk_analyzer.py        # Core risk analysis engine
│   ├── compliance_checker.py   # Regulatory compliance assessment
│   ├── cost_estimator.py       # Migration cost estimation
│   └── visualizations.py       # Plotly chart components
├── .streamlit/
│   └── config.toml             # Streamlit configuration
└── pyproject.toml              # Python dependencies
```

## Key Features

### 1. Risk Analysis Module (`modules/risk_analyzer.py`)
- **Quantum Vulnerability Analysis**: Assesses cryptographic algorithms against quantum computing threats
- **Threat Timeline Estimation**: Calculates years until quantum threat materialization
- **Threat Classification**: Categorizes risks as CRITICAL, HIGH, MEDIUM, LOW, MINIMAL
- **Migration Priority Scoring**: Ranks assets by urgency of migration need

### 2. Compliance Checker (`modules/compliance_checker.py`)
- Evaluates compliance against major regulations: NIST, PCI-DSS, GDPR, SOX, Basel III, FFIEC, ISO 27001, SWIFT CSP
- Generates gap analysis and remediation steps
- Calculates overall compliance score

### 3. Cost Estimator (`modules/cost_estimator.py`)
- Phase-based migration cost calculation
- ROI analysis over 10-year horizon
- Scenario comparison (Aggressive, Standard, Conservative)
- Timeline and Gantt chart generation

### 4. Visualizations (`modules/visualizations.py`)
- Risk heatmaps
- Threat timeline charts
- Migration priority rankings
- Cost breakdown pie charts
- ROI analysis charts
- Compliance gauge meters
- Algorithm vulnerability radar charts

## Technologies Used
- **Python 3.11**
- **Streamlit**: Web dashboard framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations
- **Plotly**: Interactive visualizations

## Running the Application
```bash
streamlit run app.py --server.port 5000
```

## Configuration Options
The sidebar provides configuration for:
- Bank Name and Size (Small, Medium, Large, Enterprise)
- Quantum Advancement Factor (0.5x - 2.0x)
- Current Quantum Readiness Level
- Risk Tolerance

## Sample Data
The application includes a sample bank cryptographic inventory with 10 assets covering:
- Core Banking TLS (RSA-2048)
- Payment Gateway (RSA-4096)
- Customer Authentication (ECC-256)
- Mobile Banking (ECC-384)
- Data Storage (AES-256)
- And more...

## Report Generation
- Executive Summary Report (Markdown)
- Technical Assessment Report (CSV)
- Compliance Gap Report (CSV)

## Recent Changes
- **January 2026**: Initial release with full feature set
  - Core risk analysis engine
  - Compliance assessment module
  - Cost estimation and ROI analysis
  - Interactive dashboard with visualizations
