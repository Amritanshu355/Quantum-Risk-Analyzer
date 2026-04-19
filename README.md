# 🔐 Quantum Risk Analyzer v2.0

## Enterprise Cryptographic Assessment Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.53+-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

**Quantum Risk Analyzer** is an enterprise-grade platform for assessing quantum computing threats to banking cryptographic infrastructure. Built for security teams, compliance officers, and C-suite executives to understand, prioritize, and plan cryptographic migrations.

![Dashboard Preview](docs/image-1.png)

---

## ✨ Features

### 🔍 Core Capabilities

| Feature | Description |
|---------|-------------|
| **Risk Analysis** | Comprehensive vulnerability assessment of cryptographic assets against quantum threats |
| **AI Recommendations** | Machine-generated prioritized action items with effort estimates |
| **Compliance Checker** | Automated assessment against FFIEC, PCI-DSS, GDPR, SOX, NIST, and more |
| **Cost Estimation** | Phase-based migration cost calculation with ROI analysis |
| **3D Visualizations** | Interactive risk surface analysis and threat timeline projections |
| **Executive Reports** | One-click report generation for different stakeholder audiences |

### 🎯 New in v2.0

- **AI-Powered Recommendations Engine** - Context-aware migration recommendations
- **3D Risk Surface Visualization** - Interactive 3D analysis of vulnerability vs timeline
- **Crypto-Agility Scoring** - Radar chart assessment of organizational readiness
- **Modern UI/UX** - Professional gradient design with animations
- **15-Year Threat Forecast** - Projection of when assets will be at risk
- **Migration Roadmap** - Phase-based visualization of migration priorities

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/quantum-risk-analyzer.git
cd quantum-risk-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install and run
uv pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Usage Guide

### 1. Configure Your Bank Profile

Use the sidebar to set:
- **Bank Name & Size** - Affects cost estimates and compliance requirements
- **Quantum Advancement Factor** - Simulate faster/slower quantum progress (0.5x - 2.0x)
- **Current Quantum Readiness** - Your organization's preparedness level
- **Risk Tolerance** - Impacts migration priority calculations

### 2. Add Cryptographic Assets

Either:
- ✅ Use the **Sample Bank Inventory** for demonstration
- ➕ Manually add assets via the **Asset Management** tab

### 3. Review the Dashboard

The home dashboard shows:
- Critical and high-risk asset counts
- Average vulnerability score
- Total migration cost estimate
- Time window until quantum threat

### 4. Explore Analysis Tabs

| Tab | Purpose |
|-----|---------|
| 📊 Risk Analysis | Heatmaps, timelines, and priority matrices |
| 📜 Compliance | Regulatory gap analysis and remediation actions |
| 💰 Cost Estimation | Budget planning and ROI projections |
| 🤖 AI Recommendations | Prioritized action items |
| 🏦 Asset Management | Add/remove cryptographic assets |
| 📋 Reports | Download executive and technical reports |

---

## 🏗️ Architecture

```
quantum-risk-analyzer/
├── app.py                      # Main Streamlit application
├── modules/
│   ├── __init__.py            # Module exports
│   ├── risk_analyzer.py       # Core risk analysis engine
│   ├── compliance_checker.py  # Regulatory compliance assessment
│   ├── cost_estimator.py      # Migration cost calculations
│   ├── visualizations.py      # Plotly chart components
│   ├── ai_recommendations.py  # AI recommendation engine (NEW)
│   └── dashboard_components.py # Modern UI components (NEW)
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.template.toml  # Secrets template
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project metadata
└── README.md                 # This file
```

---

## 🧪 Sample Data

The application includes a realistic sample bank inventory with 10 cryptographic assets:

| Asset | Algorithm | Usage Area | Sensitivity |
|-------|-----------|------------|-------------|
| Core Banking TLS | RSA-2048 | Core Banking | Critical |
| Payment Gateway | RSA-4096 | Payment Processing | Critical |
| Customer Auth Keys | ECC-256 | Customer Authentication | High |
| Mobile App Signing | ECC-384 | Mobile Banking | High |
| Data-at-Rest | AES-256 | Data Storage | Critical |
| API Gateway | RSA-2048 | API Security | Medium |
| ATM Communication | 3DES | ATM Network | High |
| Internal Email | RSA-2048 | Internal Communications | Low |
| Database Encryption | AES-128 | Data Storage | High |
| Digital Signatures | SHA-256 | Core Banking | Critical |

---

## 📈 Compliance Frameworks

The compliance checker evaluates against:

- **FFIEC** - Federal Financial Institutions Examination Council
- **PCI-DSS** - Payment Card Industry Data Security Standard
- **GDPR** - General Data Protection Regulation
- **SOX** - Sarbanes-Oxley Act
- **NIST SP 800-208** - Post-Quantum Cryptography Standards
- **SWIFT CSP** - SWIFT Customer Security Programme
- **ISO 27001** - Information Security Management
- **Basel III** - Banking Regulatory Framework

---

## 🎨 Customization

### Theme Colors

Edit `.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Custom CSS

Add your own styles in `app.py` by modifying the `CUSTOM_CSS` string.

---

## ☁️ Deploy to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/quantum-risk-analyzer.git
git push -u origin main
```

### Step 2: Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New App"**
3. Select your repository
4. Set the main file path to `app.py`
5. Click **"Deploy!"**

### Step 3: Configure (Optional)

For private repos or custom settings, add a `.streamlit/secrets.toml` file.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NIST** for Post-Quantum Cryptography standards
- **Streamlit** for the amazing web framework
- **Plotly** for interactive visualizations

---

## 📬 Contact

- **Project Link**: [GitHub Repository](https://github.com/yourusername/quantum-risk-analyzer)
- **Issues**: [Report a Bug](https://github.com/yourusername/quantum-risk-analyzer/issues)

---

*Built with ❤️ for the quantum-safe future*
