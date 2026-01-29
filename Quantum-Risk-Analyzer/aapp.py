import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from modules.risk_analyzer import (
    QuantumVulnerabilityAnalyzer, BankCryptoInventory, CryptoAsset,
    CryptoAlgorithm, generate_risk_report, ThreatLevel
)
from modules.compliance_checker import QuantumComplianceChecker, RegulatoryBody
from modules.cost_estimator import QuantumMigrationCostEstimator, MigrationPhase
from modules.visualizations import (
    create_risk_heatmap, create_threat_timeline_chart, create_migration_priority_chart,
    create_cost_breakdown_chart, create_timeline_gantt_chart, create_roi_chart,
    create_compliance_gauge, create_algorithm_vulnerability_radar,
    create_threat_distribution_pie, create_cost_vs_risk_scatter
)

st.set_page_config(
    page_title="Quantum Computing Risk Analyst",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .risk-critical { color: #E74C3C; font-weight: bold; }
    .risk-high { color: #E67E22; font-weight: bold; }
    .risk-medium { color: #F1C40F; font-weight: bold; }
    .risk-low { color: #2ECC71; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if 'risk_data' not in st.session_state:
        st.session_state.risk_data = None
    if 'custom_assets' not in st.session_state:
        st.session_state.custom_assets = []
    if 'analysis_run' not in st.session_state:
        st.session_state.analysis_run = False


def render_sidebar():
    st.sidebar.image("https://img.icons8.com/fluency/96/quantum-computing.png", width=80)
    st.sidebar.title("Configuration")
    
    st.sidebar.header("Bank Profile")
    bank_name = st.sidebar.text_input("Bank Name", value="Sample Bank Corp")
    bank_size = st.sidebar.selectbox(
        "Bank Size",
        ["Small", "Medium", "Large", "Enterprise"],
        index=2
    )
    
    st.sidebar.header("Quantum Scenario")
    quantum_advancement = st.sidebar.slider(
        "Quantum Advancement Factor",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher values simulate faster quantum computing advancement"
    )
    
    quantum_readiness = st.sidebar.selectbox(
        "Current Quantum Readiness",
        ["None", "Low", "Medium", "High"],
        index=1
    )
    
    risk_tolerance = st.sidebar.selectbox(
        "Risk Tolerance",
        ["Low", "Medium", "High"],
        index=1
    )
    
    st.sidebar.header("Analysis Options")
    use_sample_data = st.sidebar.checkbox("Use Sample Bank Inventory", value=True)
    
    return {
        "bank_name": bank_name,
        "bank_size": bank_size,
        "quantum_advancement": quantum_advancement,
        "quantum_readiness": quantum_readiness,
        "risk_tolerance": risk_tolerance,
        "use_sample_data": use_sample_data
    }


def render_header():
    st.markdown('<h1 class="main-header">Quantum Computing Risk Analyst for Banks</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align: center; color: #666; font-size: 1.1rem;">
        Comprehensive quantum computing threat assessment and migration planning platform
    </p>
    """, unsafe_allow_html=True)


def render_executive_summary(risk_data: pd.DataFrame, config: dict):
    st.header("Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = len(risk_data[risk_data['Threat Level'] == 'CRITICAL'])
    high_count = len(risk_data[risk_data['Threat Level'] == 'HIGH'])
    total_assets = len(risk_data)
    avg_vulnerability = risk_data['Vulnerability Score'].mean()
    total_migration_cost = risk_data['Est. Migration Cost ($)'].sum()
    avg_years_to_threat = risk_data['Years to Threat'].mean()
    
    with col1:
        st.metric(
            label="Total Cryptographic Assets",
            value=total_assets,
            delta=f"{critical_count} Critical"
        )
    
    with col2:
        st.metric(
            label="Average Vulnerability Score",
            value=f"{avg_vulnerability:.1f}%",
            delta=f"{high_count} High Risk",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Est. Total Migration Cost",
            value=f"${total_migration_cost/1e6:.2f}M",
            delta="Full portfolio"
        )
    
    with col4:
        st.metric(
            label="Avg. Years to Threat",
            value=f"{avg_years_to_threat:.1f} yrs",
            delta="Planning window",
            delta_color="off"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Findings")
        
        if critical_count > 0:
            st.error(f"**{critical_count} assets** require immediate attention with CRITICAL threat level")
        
        vulnerable_algos = risk_data[risk_data['Vulnerability Score'] > 80]['Algorithm'].unique()
        if len(vulnerable_algos) > 0:
            st.warning(f"Highly vulnerable algorithms in use: {', '.join(vulnerable_algos)}")
        
        urgent_assets = risk_data[risk_data['Years to Threat'] < 5]['Asset Name'].tolist()
        if urgent_assets:
            st.info(f"Assets with <5 year threat window: {', '.join(urgent_assets[:3])}...")
    
    with col2:
        st.subheader("Recommended Actions")
        st.markdown("""
        1. **Immediate**: Inventory all cryptographic assets and classify by sensitivity
        2. **Short-term**: Begin pilot programs for post-quantum cryptography (PQC)
        3. **Medium-term**: Develop comprehensive migration roadmap
        4. **Long-term**: Implement crypto-agility framework for ongoing adaptation
        """)


def render_risk_analysis_tab(risk_data: pd.DataFrame, config: dict):
    st.header("Risk Analysis Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Vulnerability Overview", "Threat Timeline", "Priority Matrix", "Detailed Analysis"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Risk Heatmap")
            heatmap = create_risk_heatmap(risk_data)
            st.plotly_chart(heatmap, use_container_width=True)
        
        with col2:
            st.subheader("Threat Level Distribution")
            pie_chart = create_threat_distribution_pie(risk_data)
            st.plotly_chart(pie_chart, use_container_width=True)
        
        st.subheader("Algorithm Vulnerability Radar")
        radar = create_algorithm_vulnerability_radar(risk_data)
        st.plotly_chart(radar, use_container_width=True)
    
    with tab2:
        st.subheader("Quantum Threat Timeline")
        timeline_chart = create_threat_timeline_chart(risk_data)
        st.plotly_chart(timeline_chart, use_container_width=True)
        
        st.info("""
        **Understanding the Timeline:**
        - Assets below the 5-year critical threshold require immediate migration planning
        - Assets below the 10-year planning horizon should be included in medium-term roadmap
        - Quantum advancement factor affects all timelines proportionally
        """)
    
    with tab3:
        st.subheader("Migration Priority Matrix")
        priority_chart = create_migration_priority_chart(risk_data)
        st.plotly_chart(priority_chart, use_container_width=True)
        
        st.subheader("Cost vs. Vulnerability Analysis")
        scatter = create_cost_vs_risk_scatter(risk_data)
        st.plotly_chart(scatter, use_container_width=True)
    
    with tab4:
        st.subheader("Detailed Asset Analysis")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            threat_filter = st.multiselect(
                "Filter by Threat Level",
                options=risk_data['Threat Level'].unique().tolist(),
                default=risk_data['Threat Level'].unique().tolist()
            )
        
        with filter_col2:
            usage_filter = st.multiselect(
                "Filter by Usage Area",
                options=risk_data['Usage Area'].unique().tolist(),
                default=risk_data['Usage Area'].unique().tolist()
            )
        
        with filter_col3:
            min_vuln = st.slider("Minimum Vulnerability Score", 0, 100, 0)
        
        filtered_data = risk_data[
            (risk_data['Threat Level'].isin(threat_filter)) &
            (risk_data['Usage Area'].isin(usage_filter)) &
            (risk_data['Vulnerability Score'] >= min_vuln)
        ]
        
        st.dataframe(
            filtered_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Vulnerability Score": st.column_config.ProgressColumn(
                    "Vulnerability Score",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Est. Migration Cost ($)": st.column_config.NumberColumn(
                    "Est. Migration Cost ($)",
                    format="$%d"
                )
            }
        )


def render_compliance_tab(config: dict):
    st.header("Regulatory Compliance Assessment")
    
    checker = QuantumComplianceChecker(
        bank_size=config["bank_size"],
        quantum_readiness_level=config["quantum_readiness"]
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        compliance_score = checker.calculate_overall_compliance_score()
        gauge = create_compliance_gauge(compliance_score)
        st.plotly_chart(gauge, use_container_width=True)
        
        if compliance_score < 30:
            st.error("Critical compliance gaps detected. Immediate action required.")
        elif compliance_score < 50:
            st.warning("Significant compliance improvements needed.")
        elif compliance_score < 70:
            st.info("Moderate compliance level. Continue improvement efforts.")
        else:
            st.success("Good compliance posture. Maintain current controls.")
    
    with col2:
        st.subheader("Priority Remediation Actions")
        priority_actions = checker.get_priority_actions()
        
        if priority_actions:
            for i, action in enumerate(priority_actions[:5], 1):
                with st.expander(f"{i}. {action['Regulation']} - {action['Risk']}"):
                    st.write(f"**Action:** {action['Action']}")
                    st.write(f"**Estimated Effort:** {action['Effort']} days")
        else:
            st.success("No immediate priority actions required.")
    
    st.subheader("Detailed Compliance Report")
    compliance_report = checker.generate_compliance_report()
    
    st.dataframe(
        compliance_report,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Effort (Days)": st.column_config.NumberColumn(
                "Effort (Days)",
                format="%d days"
            )
        }
    )
    
    csv = compliance_report.to_csv(index=False)
    st.download_button(
        label="Download Compliance Report (CSV)",
        data=csv,
        file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def render_cost_tab(config: dict, risk_data: pd.DataFrame):
    st.header("Migration Cost Analysis")
    
    estimator = QuantumMigrationCostEstimator(
        bank_size=config["bank_size"],
        risk_tolerance=config["risk_tolerance"]
    )
    
    algorithms = risk_data['Algorithm'].unique().tolist()
    usage_areas = risk_data['Usage Area'].unique().tolist()
    
    estimate = estimator.calculate_total_migration_cost(
        algorithms=algorithms,
        usage_areas=usage_areas
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Estimated Cost",
            f"${estimate.total_cost/1e6:.2f}M"
        )
    
    with col2:
        st.metric(
            "Project Timeline",
            f"{estimate.timeline_months} months"
        )
    
    with col3:
        st.metric(
            "Risk Contingency",
            f"${estimate.risk_contingency/1e6:.2f}M"
        )
    
    with col4:
        st.metric(
            "ROI Breakeven",
            f"{estimate.roi_years:.1f} years"
        )
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Cost Breakdown", "Project Timeline", "ROI Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Cost Distribution")
            cost_pie = create_cost_breakdown_chart(estimate.cost_breakdown)
            st.plotly_chart(cost_pie, use_container_width=True)
        
        with col2:
            st.subheader("Cost Components")
            cost_df = pd.DataFrame([
                {"Component": k, "Cost ($)": v}
                for k, v in estimate.cost_breakdown.items()
            ])
            cost_df = cost_df.sort_values("Cost ($)", ascending=False)
            st.dataframe(
                cost_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Cost ($)": st.column_config.NumberColumn(
                        "Cost ($)",
                        format="$%d"
                    )
                }
            )
    
    with tab2:
        st.subheader("Migration Project Timeline")
        timeline_df = estimator.generate_cost_timeline()
        gantt = create_timeline_gantt_chart(timeline_df)
        st.plotly_chart(gantt, use_container_width=True)
        
        st.subheader("Phase Details")
        st.dataframe(
            timeline_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Phase Cost ($)": st.column_config.NumberColumn(
                    "Phase Cost ($)",
                    format="$%d"
                ),
                "Cumulative Cost ($)": st.column_config.NumberColumn(
                    "Cumulative Cost ($)",
                    format="$%d"
                )
            }
        )
    
    with tab3:
        st.subheader("Return on Investment Analysis")
        roi_df = estimator.generate_roi_analysis(estimate)
        roi_chart = create_roi_chart(roi_df, estimate.total_cost)
        st.plotly_chart(roi_chart, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("10-Year ROI Projection")
            st.dataframe(
                roi_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Annual Risk Savings ($)": st.column_config.NumberColumn(format="$%d"),
                    "Cumulative Savings ($)": st.column_config.NumberColumn(format="$%d"),
                    "Net Benefit ($)": st.column_config.NumberColumn(format="$%d"),
                    "ROI (%)": st.column_config.NumberColumn(format="%.1f%%")
                }
            )
        
        with col2:
            st.subheader("Scenario Comparison")
            scenarios = estimator.compare_scenarios()
            st.dataframe(
                scenarios,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Total Cost ($)": st.column_config.NumberColumn(format="$%d"),
                    "ROI (Years)": st.column_config.NumberColumn(format="%.1f")
                }
            )


def render_asset_management_tab(config: dict):
    st.header("Cryptographic Asset Management")
    
    st.subheader("Add New Cryptographic Asset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        asset_name = st.text_input("Asset Name", placeholder="e.g., Payment Gateway TLS")
        algorithm = st.selectbox(
            "Cryptographic Algorithm",
            options=[algo.value for algo in CryptoAlgorithm]
        )
        usage_area = st.selectbox(
            "Usage Area",
            options=["Core Banking", "Payment Processing", "Customer Authentication",
                    "Internal Communications", "Data Storage", "API Security",
                    "Mobile Banking", "ATM Network"]
        )
    
    with col2:
        key_size = st.number_input("Key Size (bits)", min_value=64, max_value=8192, value=2048)
        data_sensitivity = st.selectbox(
            "Data Sensitivity",
            options=["Critical", "High", "Medium", "Low"]
        )
        data_volume = st.number_input("Estimated Data Volume (GB)", min_value=1, max_value=100000, value=100)
    
    if st.button("Add Asset to Inventory"):
        new_asset = {
            "name": asset_name,
            "algorithm": algorithm,
            "key_size": key_size,
            "usage_area": usage_area,
            "data_sensitivity": data_sensitivity,
            "data_volume": data_volume
        }
        st.session_state.custom_assets.append(new_asset)
        st.success(f"Added asset: {asset_name}")
    
    if st.session_state.custom_assets:
        st.subheader("Custom Assets Added")
        custom_df = pd.DataFrame(st.session_state.custom_assets)
        st.dataframe(custom_df, use_container_width=True, hide_index=True)
        
        if st.button("Clear All Custom Assets"):
            st.session_state.custom_assets = []
            st.rerun()


def render_reports_tab(risk_data: pd.DataFrame, config: dict):
    st.header("Report Generation")
    
    st.subheader("Available Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Executive Summary Report")
        st.write("High-level overview for board and C-suite")
        if st.button("Generate Executive Report"):
            report_content = generate_executive_report(risk_data, config)
            st.download_button(
                "Download Executive Report",
                report_content,
                file_name=f"executive_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
    
    with col2:
        st.markdown("### Technical Assessment Report")
        st.write("Detailed technical analysis for IT teams")
        csv = risk_data.to_csv(index=False)
        st.download_button(
            "Download Technical Report (CSV)",
            csv,
            file_name=f"technical_assessment_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col3:
        st.markdown("### Compliance Gap Report")
        st.write("Regulatory compliance status and gaps")
        checker = QuantumComplianceChecker(
            bank_size=config["bank_size"],
            quantum_readiness_level=config["quantum_readiness"]
        )
        compliance_csv = checker.generate_compliance_report().to_csv(index=False)
        st.download_button(
            "Download Compliance Report (CSV)",
            compliance_csv,
            file_name=f"compliance_gaps_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def generate_executive_report(risk_data: pd.DataFrame, config: dict) -> str:
    critical_count = len(risk_data[risk_data['Threat Level'] == 'CRITICAL'])
    high_count = len(risk_data[risk_data['Threat Level'] == 'HIGH'])
    total_cost = risk_data['Est. Migration Cost ($)'].sum()
    avg_timeline = risk_data['Years to Threat'].mean()
    
    report = f"""# Quantum Computing Risk Assessment
## Executive Summary Report

**Bank Name:** {config['bank_name']}
**Assessment Date:** {datetime.now().strftime('%B %d, %Y')}
**Bank Size Category:** {config['bank_size']}

---

## Key Findings

### Threat Overview
- **Total Cryptographic Assets Analyzed:** {len(risk_data)}
- **Critical Threat Assets:** {critical_count}
- **High Threat Assets:** {high_count}
- **Average Time to Quantum Threat:** {avg_timeline:.1f} years

### Financial Impact
- **Estimated Total Migration Cost:** ${total_cost/1e6:.2f} million
- **Average Migration Cost per Asset:** ${total_cost/len(risk_data):,.0f}

### Risk Distribution
"""
    
    for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
        count = len(risk_data[risk_data['Threat Level'] == level])
        pct = (count / len(risk_data)) * 100
        report += f"- {level}: {count} assets ({pct:.1f}%)\n"
    
    report += f"""
---

## Recommendations

1. **Immediate Actions (0-6 months)**
   - Complete comprehensive cryptographic inventory
   - Prioritize migration of CRITICAL assets
   - Establish quantum readiness governance committee

2. **Short-term Actions (6-18 months)**
   - Begin pilot programs for post-quantum cryptography
   - Develop detailed migration roadmap
   - Train security teams on quantum threats

3. **Medium-term Actions (18-36 months)**
   - Execute phased migration of HIGH risk assets
   - Implement crypto-agility framework
   - Regular reassessment of quantum threat timeline

---

*Report generated by Quantum Computing Risk Analyst*
*Configuration: Quantum Advancement Factor = {config['quantum_advancement']}, Readiness = {config['quantum_readiness']}*
"""
    
    return report


def main():
    init_session_state()
    config = render_sidebar()
    render_header()
    
    if config["use_sample_data"]:
        inventory = BankCryptoInventory()
        assets = inventory.get_sample_bank_inventory()
    else:
        if st.session_state.custom_assets:
            assets = [
                CryptoAsset(
                    name=a["name"],
                    algorithm=CryptoAlgorithm(a["algorithm"]),
                    key_size=a["key_size"],
                    usage_area=a["usage_area"],
                    data_sensitivity=a["data_sensitivity"],
                    estimated_data_volume_gb=a["data_volume"]
                )
                for a in st.session_state.custom_assets
            ]
        else:
            st.warning("No custom assets added. Please add assets in the Asset Management tab or enable 'Use Sample Bank Inventory' in the sidebar.")
            assets = []
    
    if assets:
        risk_data = generate_risk_report(assets, config["quantum_advancement"])
        st.session_state.risk_data = risk_data
        
        render_executive_summary(risk_data, config)
        
        st.markdown("---")
        
        tabs = st.tabs([
            "Risk Analysis",
            "Compliance",
            "Cost Estimation",
            "Asset Management",
            "Reports"
        ])
        
        with tabs[0]:
            render_risk_analysis_tab(risk_data, config)
        
        with tabs[1]:
            render_compliance_tab(config)
        
        with tabs[2]:
            render_cost_tab(config, risk_data)
        
        with tabs[3]:
            render_asset_management_tab(config)
        
        with tabs[4]:
            render_reports_tab(risk_data, config)
    else:
        st.header("Getting Started")
        st.info("""
        Welcome to the Quantum Computing Risk Analyst for Banks!
        
        To begin your analysis:
        1. Enable 'Use Sample Bank Inventory' in the sidebar to see a demo, OR
        2. Go to the Asset Management tab to add your bank's cryptographic assets
        """)
        
        tabs = st.tabs(["Asset Management"])
        with tabs[0]:
            render_asset_management_tab(config)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.8rem;">
        <p>Quantum Risk Analyst v1.0</p>
        <p>Built for Banking Security</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
