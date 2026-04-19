# Quantum Computing Risk Analyzer - System Design

## Overview

The **Quantum Computing Risk Analyzer** is a comprehensive enterprise application designed to help banks and financial institutions assess, analyze, and mitigate quantum computing threats to their cryptographic infrastructure.

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         User Interface (Streamlit)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Risk Analysis │  │ File Upload  │  │ Compliance   │  │ Cost      │ │
│  │ Dashboard    │  │ & Inventory  │  │ Checker      │  │ Estimator │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └───────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ AI Recomm.   │  │ Asset Mgmt   │  │ Reports      │  │ ...       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Core Application Logic                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Streamlit App Controller (app.py)                               │  │
│  │  • Session State Management                                      │  │
│  │  • UI Routing & Component Rendering                             │  │
│  │  • Event Handling & User Interactions                            │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Risk Analysis   │    │  Compliance      │    │  Cost Estimation │
│  Engine          │    │  Checker         │    │  Engine          │
│  (risk_analyzer  │    │  (compliance_    │    │  (cost_estimator  │
│   .py)           │    │   checker.py)    │    │   .py)           │
└──────────────────┘    └──────────────────┘    └──────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Business Logic Modules                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │ AI               │  │ File             │  │ Dashboard        │  │
│  │ Recommendations  │  │ Parser           │  │ Components       │  │
│  │ (ai_recommendations  │ (file_parser.py) │  │ (dashboard_     │  │
│  │  .py)            │  │                  │  │  components.py)  │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Visualization Engine (visualizations.py)                        │  │
│  │  • Risk Heatmaps                                                 │  │
│  │  • Timeline Charts                                               │  │
│  │  • Pie Charts & Bar Charts                                      │  │
│  │  • Gantt Timelines & Radar Plots                                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Data & Configuration Layer                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │ Sample Data      │  │ User Uploaded    │  │ Configuration    │  │
│  │ (Built-in)       │  │ Files (CSV/Excel)│  │ (Bank Settings)  │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐                           │
│  │ Session State    │  │ Report           │                           │
│  │ (Streamlit)      │  │ Generation       │                           │
│  └──────────────────┘  └──────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. User Interface Layer

**File: `app.py`**

This is the main entry point and UI controller of the application.

**Responsibilities:**
- Page configuration and theme management
- Sidebar configuration (bank settings)
- Tab-based UI navigation
- Component rendering
- Session state management
- Event handling and user interactions

**Key Components:**
- Executive Summary dashboard (metrics cards)
- Risk Analysis tab (visualizations)
- File Upload tab (Excel/CSV import)
- Compliance tab (regulatory checks)
- Cost Analysis tab (ROI & migration costs)
- AI Recommendations tab
- Asset Management tab
- Reports tab (downloads)

---

### 2. Core Analysis Modules

#### 2.1 Risk Analysis Engine
**File: `modules/risk_analyzer.py`**

**Responsibilities:**
- Cryptographic vulnerability assessment
- Quantum threat timeline calculation
- Threat level classification (CRITICAL/HIGH/MEDIUM/LOW/MINIMAL)
- Risk scoring and prioritization
- Sample data generation

**Key Classes:**
- `CryptoAlgorithm`: Represents cryptographic algorithms with properties
- `CryptoAsset`: Represents a bank's crypto asset with risk metadata
- `BankCryptoInventory`: Manages collection of crypto assets
- `QuantumVulnerabilityAnalyzer`: Core analysis engine
- `ThreatLevel`: Enum for threat classification

**Core Calculations:**
```
Vulnerability Score = f(algorithm_age, key_size, known_attacks)
Years to Threat = f(algorithm_strength, quantum_progress)
Migration Priority = f(threat_level, data_sensitivity, business_impact)
```

---

#### 2.2 Compliance Checker
**File: `modules/compliance_checker.py`**

**Responsibilities:**
- Regulatory compliance assessment
- Framework evaluation (NIST, GDPR, PCI-DSS, etc.)
- Compliance gap analysis
- Compliance score calculation
- Report generation

**Regulatory Frameworks:**
- NIST SP 800-186 (PQC Standards)
- GDPR (EU Data Protection)
- PCI-DSS (Payment Card Security)
- HIPAA (Healthcare)
- NY DFS 23 NYCRR 500
- EBA Guidelines on ICT Risk
- ISO 27001/27002
- MAS TRM (Singapore)

---

#### 2.3 Cost Estimation Engine
**File: `modules/cost_estimator.py`**

**Responsibilities:**
- Migration cost calculation
- ROI (Return on Investment) analysis
- Timeline and phase planning
- Cost breakdown by category
- Savings projections

**Cost Categories:**
- Assessment & Planning
- Software & Licensing
- Hardware Upgrades
- Implementation
- Training
- Testing & Validation
- Ongoing Maintenance

---

#### 2.4 AI Recommendation Engine
**File: `modules/ai_recommendations.py`**

**Responsibilities:**
- Intelligent migration recommendations
- Priority-based action planning
- Risk mitigation strategies
- Phased migration planning

**Recommendation Types:**
- Immediate Action Required
- Prioritize for This Year
- Schedule for Next 2-3 Years
- Monitor and Plan
- Continue Monitoring

---

#### 2.5 File Parser
**File: `modules/file_parser.py`**

**Responsibilities:**
- Excel/CSV file parsing
- Data validation and cleaning
- Algorithm name normalization
- Smart column matching
- Inventory data import

**Supported Formats:**
- Excel (.xlsx, .xls)
- CSV (.csv)

**Required Columns:**
- Asset Name
- Algorithm
- Key Size
- Usage Area
- Data Sensitivity
- Data Volume (GB)

---

#### 2.6 Visualization Engine
**File: `modules/visualizations.py`**

**Responsibilities:**
- Data visualization and charting
- Interactive Plotly charts
- Theme management (light/dark)
- Dashboard component rendering

**Chart Types:**
1. **Risk Heatmap** - Algorithm vs Usage Area vulnerability
2. **Threat Timeline** - Years to quantum threat by asset
3. **Migration Priority** - Priority ranking horizontal bars
4. **Cost Breakdown** - Pie chart of migration costs
5. **Gantt Timeline** - Migration phases and durations
6. **ROI Chart** - Return on Investment over time
7. **Compliance Gauge** - Overall compliance score indicator
8. **Vulnerability Radar** - Algorithm vulnerability comparison
9. **Threat Distribution** - Pie chart of threat levels
10. **Cost vs Risk Scatter** - Cost vs vulnerability relationship

---

## Data Flow Architecture

### Data Flow Diagram

```
User Input
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ Streamlit UI (app.py)                                       │
│ • Configuration Settings (Bank Name, Size, etc.)           │
│ • File Upload (CSV/Excel)                                   │
│ • User Interactions (Button Clicks, Tabs)                  │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────────────────────┐
    │                                       │
    ▼                                       ▼
┌──────────────────┐             ┌──────────────────┐
│ File Parser      │             │ Configuration    │
│ (file_parser.py) │             │ (Session State)  │
└──────────────────┘             └──────────────────┘
    │                                       │
    └──────────────┬────────────────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │ Data Processing Layer    │
        │ • Data Cleaning          │
        │ • Algorithm Normalization│
        │ • Validation             │
        └──────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Risk    │  │Compliance│  │Cost     │
│ Analysis│  │ Checker │  │Estimator│
└─────────┘  └─────────┘  └─────────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │ AI Recommendation        │
        │ Engine                   │
        └──────────────────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │ Visualization Engine     │
        │ (visualizations.py)      │
        └──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ Streamlit UI Rendering (app.py)                            │
│ • Display Metrics                                           │
│ • Show Charts & Visualizations                             │
│ • Render Tables & Dataframes                               │
│ • Generate Reports                                          │
└─────────────────────────────────────────────────────────────┘
                   │
                   ▼
              User Output
```

---

## Key Data Structures

### 1. Crypto Asset Data Model
```python
{
    "asset_name": str,           # Unique asset identifier
    "algorithm": str,            # Cryptographic algorithm used
    "key_size": int,             # Key size in bits
    "usage_area": str,           # Business usage area
    "data_sensitivity": str,     # HIGH/MEDIUM/LOW
    "data_volume_gb": float,     # Data volume in GB
    "vulnerability_score": float,# 0-100 vulnerability score
    "years_to_threat": float,    # Years until quantum threat
    "threat_level": str,         # CRITICAL/HIGH/MEDIUM/LOW/MINIMAL
    "migration_priority": int,   # Priority score 0-100
    "migration_cost": float      # Estimated migration cost ($)
}
```

### 2. Configuration Model
```python
{
    "bank_name": str,
    "bank_size": str,            # Small/Medium/Large/Enterprise
    "annual_revenue": float,
    "geographic_presence": str,
    "quantum_readiness": str,    # Basic/Developing/Advanced/Leader
    "migration_timeline": int,    # Years
    "risk_tolerance": str,       # Conservative/Moderate/Aggressive
    "compliance_frameworks": List[str]
}
```

### 3. Cost Estimation Model
```python
{
    "total_cost": float,
    "phases": [
        {
            "phase": str,
            "start_month": int,
            "duration_months": int,
            "phase_cost": float
        }
    ],
    "roi_years": [
        {
            "year": int,
            "cumulative_savings": float,
            "net_benefit": float,
            "roi_percent": float
        }
    ]
}
```

---

## Technology Stack

### Frontend
- **Streamlit**: Modern web application framework
- **Plotly**: Interactive data visualization
- **Pandas**: Data manipulation and analysis

### Backend & Core
- **Python 3.12+**: Primary programming language
- **NumPy**: Numerical computations
- **Dataclasses**: Data modeling
- **Enums**: Type-safe constants

### Data & Storage
- **In-memory DataFrames**: Session-based data storage
- **File-based**: CSV/Excel import
- **Streamlit Session State**: Application state management

### Visualization
- **Plotly Express**: High-level charting
- **Plotly Graph Objects**: Low-level customization
- **Dark/Light Theme Support**: Responsive theming

### Deployment
- **Docker**: Containerization
- **Streamlit Cloud**: Deployment platform
- **Uv/Venv**: Dependency management

---

## Deployment Architecture

### Production Deployment

```
                    ┌─────────────┐
                    │   User      │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Streamlit│    │ Streamlit│    │ Streamlit│
    │ Instance1│    │ Instance2│    │ Instance3│
    └──────┬───┘    └──────┬───┘    └──────┬───┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
            ┌──────────────┐  ┌──────────────┐
            │   File       │  │   Session    │
            │  Storage     │  │   Cache      │
            └──────────────┘  └──────────────┘
```

### Docker Containerization
**File: `Dockerfile`**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## Security Considerations

### Data Security
- All processing happens in-memory (no persistent storage)
- File uploads are temporary (Streamlit session)
- No sensitive data is logged or stored
- No external network calls (except optional API integrations)

### Application Security
- Input validation on all user inputs
- File type validation and sanitization
- No authentication (intended for internal enterprise use)
- No SQL injection (no database)

---

## Scalability & Performance

### Current Limitations
- Single-user application (Streamlit session-based)
- In-memory processing
- No distributed computing

### Scalability Improvements
- Add database backend (PostgreSQL, MongoDB)
- Implement user authentication
- Add async processing for large datasets
- Implement caching for repeated computations
- Add API layer for integration with other systems

---

## Future Enhancements

### Short-term
- User authentication and role-based access
- Database integration for persistent storage
- More file format support (PDF, JSON, XML)
- Batch processing for large datasets

### Medium-term
- Real-time quantum threat intelligence feeds
- Integration with actual quantum-safe APIs
- Multi-bank support and multi-tenant architecture
- Advanced AI/ML models for better predictions

### Long-term
- Enterprise-grade reporting and analytics
- API-first architecture
- Cloud-native deployment (Kubernetes)
- Integration with HSMs and key management systems

---

## Summary

The **Quantum Computing Risk Analyzer** is a modular, well-architected application that:

1. **Follows Separation of Concerns**: Each module has single responsibility
2. **Uses Clean Architecture**: UI, Logic, and Data layers are separated
3. **Is Easily Extensible**: New features can be added without breaking existing ones
4. **Has Professional UI**: Clean, modern interface with light/dark theme support
5. **Is Production-Ready**: Dockerized, well-documented, and tested

The system is designed to help financial institutions proactively assess and mitigate quantum computing threats to their cryptographic infrastructure!
