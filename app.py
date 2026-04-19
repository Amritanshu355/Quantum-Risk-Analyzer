"""
Quantum Computing Risk Analyzer for Banks
Modern, Resume-Worthy Edition
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
# from plotly.subplots import make_subplots  # Not used in current code

# Import modules
from modules.risk_analyzer import (
    QuantumVulnerabilityAnalyzer, BankCryptoInventory, CryptoAsset,
    CryptoAlgorithm, generate_risk_report
)
from modules.compliance_checker import QuantumComplianceChecker
from modules.cost_estimator import QuantumMigrationCostEstimator
from modules.ai_recommendations import AIRecommendationEngine, RecommendationPriority
from modules.file_parser import FileParser

# Page configuration
st.set_page_config(
    page_title="Quantum Risk Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean White Theme for Perfect Readability
CUSTOM_CSS = """
<style>
/* Global white theme - clean and professional */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    color: #1f2328 !important;
}

[data-testid="stSidebar"] {
    background-color: #f6f8fa !important;
}

/* Main container */
.main > div {
    padding: 1rem 2rem;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0969da 0%, #8250df 50%, #cf222e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;
}

.sub-header {
    text-align: center;
    color: #57606a;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

/* Metric cards */
.metric-card {
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    background: linear-gradient(135deg, #ffffff 0%, #f6f8fa 100%);
    border: 1px solid #d0d7de;
    box-shadow: 0 4px 20px rgba(9, 105, 218, 0.1);
}

/* Info boxes */
.info-box {
    background: #f6f8fa;
    border-left: 4px solid #0969da;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    border: 1px solid #d0d7de;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0969da 0%, #1f6feb 100%);
    color: white;
    border: 1px solid #0969da;
    padding: 0.6rem 1.5rem;
    border-radius: 6px;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1f6feb 0%, #0969da 100%);
    box-shadow: 0 4px 15px rgba(9, 105, 218, 0.3);
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    color: #656d76;
    font-size: 0.8rem;
    border-top: 1px solid #d0d7de;
    margin-top: 2rem;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Input fields */
input, textarea, select {
    background-color: #f6f8fa !important;
    color: #1f2328 !important;
    border-color: #d0d7de !important;
}

/* Tabs */
[data-baseweb="tab"] {
    background-color: #f6f8fa !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #0969da 0%, #1f6feb 100%) !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state"""
    defaults = {
        'risk_data': None,
        'custom_assets': [],
        'recommendations': None,
        'config': {},
        'uploaded_assets': None,
        'uploaded_file_name': None,
        'use_uploaded_data': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar():
    """Render sidebar configuration with clear explanations"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 3.5rem;">🔐</div>
            <h2 style="color: #0969da; margin: 0.5rem 0;">Quantum Risk<br/>Analyzer</h2>
            <p style="color: #57606a; font-size: 0.9rem; margin-top: 0.5rem;">Configure your quantum risk assessment</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # === Bank Information ===
        st.subheader("🏦 Bank Information")
        
        bank_name = st.text_input(
            "Bank Name",
            value="Acme Bank Corp",
            help="Enter your bank or organization name for report generation"
        )
        
        bank_size = st.selectbox(
            "Bank Size",
            ["Small", "Medium", "Large", "Enterprise"],
            index=2,
            help="""
            - Small: < 100 employees, local operations
            - Medium: 100-1000 employees, regional
            - Large: 1000-5000 employees, national
            - Enterprise: 5000+ employees, global
            """
        )

        st.markdown("---")

        # === Risk Assessment Settings ===
        st.subheader("⚙️ Risk Assessment Settings")
        
        quantum_advancement = st.slider(
            "Quantum Advancement Factor",
            0.5, 2.0, 1.0, 0.1,
            help="""
            Adjust how quickly you believe quantum computers will advance.
            
            - 0.5 = Conservative (quantum threats are further away)
            - 1.0 = Moderate (balanced timeline)
            - 2.0 = Aggressive (quantum threats are imminent)
            """
        )
        
        quantum_readiness = st.selectbox(
            "Current Quantum Readiness Level",
            ["None", "Low", "Medium", "High"],
            index=1,
            help="""
            Your organization's current quantum readiness.
            
            - None: No quantum planning started
            - Low: Initial awareness only
            - Medium: Some planning and assessment done
            - High: Active migration program in place
            """
        )
        
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["Low", "Medium", "High"],
            index=1,
            help="""
            Your organization's appetite for risk.
            
            - Low: Prioritize security, migrate early
            - Medium: Balance security and cost
            - High: Cost-conscious, migrate later
            """
        )

        st.markdown("---")

        # === Data & Features ===
        st.subheader("📊 Data & Features")
        
        use_sample_data = st.checkbox(
            "Use Sample Data",
            value=True,
            help="Use built-in sample cryptographic inventory for demonstration. Disable to upload your own data."
        )
        
        show_ai = st.checkbox(
            "Enable AI Recommendations",
            value=True,
            help="Show AI-powered migration recommendations and action plans"
        )

        st.markdown("---")

        # === Quick Stats ===
        if st.session_state.risk_data is not None:
            st.subheader("📈 Quick Stats")
            df = st.session_state.risk_data
            critical_count = len(df[df['Threat Level'] == 'CRITICAL'])
            total_count = len(df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Critical Assets",
                    critical_count,
                    help="Assets requiring immediate migration"
                )
            with col2:
                st.metric(
                    "Total Assets",
                    total_count,
                    help="All cryptographic assets in inventory"
                )
            
            if total_count > 0:
                critical_pct = (critical_count / total_count) * 100
                st.progress(critical_pct / 100, text=f"Critical: {critical_pct:.1f}%")

        return {
            "bank_name": bank_name,
            "bank_size": bank_size,
            "quantum_advancement": quantum_advancement,
            "quantum_readiness": quantum_readiness,
            "risk_tolerance": risk_tolerance,
            "use_sample_data": use_sample_data,
            "show_ai": show_ai
        }


def create_risk_gauge(df):
    """Create risk gauge chart with white theme colors"""
    critical_pct = len(df[df['Threat Level'] == 'CRITICAL']) / len(df) * 100 if len(df) > 0 else 0
    high_pct = len(df[df['Threat Level'] == 'HIGH']) / len(df) * 100 if len(df) > 0 else 0
    score = min(100, (critical_pct * 2 + high_pct + df['Vulnerability Score'].mean()) / 3) if len(df) > 0 else 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 16, 'color': '#1f2328'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#57606a'},
            'bar': {'color': "#0969da"},
            'bgcolor': "#f6f8fa",
            'bordercolor': "#d0d7de",
            'steps': [
                {'range': [0, 20], 'color': '#1a7f37'},
                {'range': [20, 40], 'color': '#3fb950'},
                {'range': [40, 60], 'color': '#d4a72c'},
                {'range': [60, 80], 'color': '#9a6700'},
                {'range': [80, 100], 'color': '#cf222e'}
            ]
        }
    ))
    fig.update_layout(height=250, paper_bgcolor="#ffffff")
    return fig


def create_threat_pie(df):
    """Create threat level pie chart with white theme colors"""
    counts = df['Threat Level'].value_counts()
    colors = {
        'CRITICAL': '#cf222e', 
        'HIGH': '#9a6700', 
        'MEDIUM': '#d4a72c', 
        'LOW': '#1a7f37', 
        'MINIMAL': '#0969da'
    }

    fig = px.pie(
        values=counts.values,
        names=counts.index,
        color=counts.index,
        color_discrete_map=colors,
        hole=0.4
    )
    fig.update_layout(
        height=350, 
        title="Threat Distribution",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f6f8fa",
        font=dict(color="#1f2328")
    )
    return fig


def create_timeline_chart(df):
    """Create threat timeline bar chart"""
    chart_df = df.sort_values('Years to Threat')

    colors = {'CRITICAL': '#E74C3C', 'HIGH': '#E67E22', 'MEDIUM': '#F1C40F', 'LOW': '#2ECC71', 'MINIMAL': '#3498DB'}
    bar_colors = [colors.get(level, '#95A5A6') for level in chart_df['Threat Level']]

    fig = go.Figure(go.Bar(
        x=chart_df['Asset Name'],
        y=chart_df['Years to Threat'],
        marker_color=bar_colors,
        text=chart_df['Years to Threat'].round(1)
    ))

    fig.add_hline(y=5, line_dash="dash", line_color="red", annotation_text="Critical (5 yrs)")
    fig.update_layout(
        title="Threat Timeline",
        xaxis_title="Asset",
        yaxis_title="Years to Threat",
        xaxis_tickangle=-45,
        height=400
    )
    return fig


def create_priority_chart(df):
    """Create migration priority chart"""
    chart_df = df.sort_values('Migration Priority', ascending=True)

    fig = px.bar(
        x=chart_df['Migration Priority'],
        y=chart_df['Asset Name'],
        orientation='h',
        color=chart_df['Threat Level'],
        color_discrete_map={'CRITICAL': '#E74C3C', 'HIGH': '#E67E22', 'MEDIUM': '#F1C40F', 'LOW': '#2ECC71', 'MINIMAL': '#3498DB'},
        title="Migration Priority"
    )
    fig.update_layout(height=400, xaxis_title="Priority Score")
    return fig


def create_cost_pie(estimate):
    """Create cost breakdown pie chart"""
    labels = list(estimate.cost_breakdown.keys())
    values = list(estimate.cost_breakdown.values())

    fig = px.pie(values=values, names=labels, hole=0.4, title="Cost Breakdown")
    fig.update_layout(height=350)
    return fig


def render_dashboard(df, config):
    """Render main dashboard"""

    # Metrics
    critical = len(df[df['Threat Level'] == 'CRITICAL'])
    high = len(df[df['Threat Level'] == 'HIGH'])
    avg_vuln = df['Vulnerability Score'].mean()
    total_cost = df['Est. Migration Cost ($)'].sum()
    avg_years = df['Years to Threat'].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    colors = ["#E74C3C", "#E67E22", "#3498DB", "#9B59B6", "#2ECC71"]

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {colors[0]}20, {colors[0]}40);">
            <div style="font-size: 2rem;">🔴</div>
            <div style="font-size: 0.8rem; color: #666;">CRITICAL</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: {colors[0]};">{critical}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {colors[1]}20, {colors[1]}40);">
            <div style="font-size: 2rem;">🟠</div>
            <div style="font-size: 0.8rem; color: #666;">HIGH RISK</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: {colors[1]};">{high}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {colors[2]}20, {colors[2]}40);">
            <div style="font-size: 2rem;">📊</div>
            <div style="font-size: 0.8rem; color: #666;">AVG VULN</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: {colors[2]};">{avg_vuln:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {colors[3]}20, {colors[3]}40);">
            <div style="font-size: 2rem;">💰</div>
            <div style="font-size: 0.8rem; color: #666;">COST</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: {colors[3]};">${total_cost/1e6:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {colors[4]}20, {colors[4]}40);">
            <div style="font-size: 2rem;">⏱️</div>
            <div style="font-size: 0.8rem; color: #666;">TIME WINDOW</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: {colors[4]};">{avg_years:.1f} yrs</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_risk_gauge(df), use_container_width=True)

    with col2:
        st.plotly_chart(create_threat_pie(df), use_container_width=True)


def render_risk_analysis(df):
    """Render risk analysis tab"""

    tab1, tab2, tab3 = st.tabs(["Timeline", "Priority", "Details"])

    with tab1:
        st.plotly_chart(create_timeline_chart(df), use_container_width=True)

    with tab2:
        st.plotly_chart(create_priority_chart(df), use_container_width=True)

    with tab3:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Vulnerability Score": st.column_config.ProgressColumn(
                    "Vuln %",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                ),
                "Est. Migration Cost ($)": st.column_config.NumberColumn(format="$%d")
            }
        )


def render_compliance(config):
    """Render compliance tab"""

    checker = QuantumComplianceChecker(
        bank_size=config["bank_size"],
        quantum_readiness_level=config["quantum_readiness"]
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        score = checker.calculate_overall_compliance_score()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Compliance Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#0F4C75"},
                'steps': [
                    {'range': [0, 30], 'color': '#E74C3C'},
                    {'range': [30, 50], 'color': '#E67E22'},
                    {'range': [50, 70], 'color': '#F1C40F'},
                    {'range': [70, 100], 'color': '#27AE60'}
                ]
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Priority Actions")
        actions = checker.get_priority_actions()
        for i, action in enumerate(actions[:5], 1):
            with st.expander(f"{i}. {action['Regulation']} - {action['Risk']}"):
                st.write(f"**Action:** {action['Action']}")
                st.write(f"**Effort:** {action['Effort']} days")

    st.subheader("Full Compliance Report")
    report = checker.generate_compliance_report()
    st.dataframe(report, use_container_width=True, hide_index=True)

    csv = report.to_csv(index=False)
    st.download_button("📥 Download CSV", csv, "compliance_report.csv", "text/csv")


def render_cost_analysis(df, config):
    """Render cost analysis tab"""

    estimator = QuantumMigrationCostEstimator(
        bank_size=config["bank_size"],
        risk_tolerance=config["risk_tolerance"]
    )

    estimate = estimator.calculate_total_migration_cost(
        algorithms=df['Algorithm'].unique().tolist(),
        usage_areas=df['Usage Area'].unique().tolist()
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cost", f"${estimate.total_cost/1e6:.2f}M")
    col2.metric("Timeline", f"{estimate.timeline_months} months")
    col3.metric("Risk Contingency", f"${estimate.risk_contingency/1e6:.2f}M")
    col4.metric("ROI Breakeven", f"{estimate.roi_years:.1f} years")

    st.markdown("---")

    tab1, tab2 = st.tabs(["Cost Breakdown", "ROI Analysis"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_cost_pie(estimate), use_container_width=True)
        with col2:
            cost_df = pd.DataFrame([
                {"Component": k, "Cost ($)": v}
                for k, v in estimate.cost_breakdown.items()
            ])
            st.dataframe(cost_df.sort_values("Cost ($)", ascending=False), use_container_width=True, hide_index=True)

    with tab2:
        roi_df = estimator.generate_roi_analysis(estimate)
        st.dataframe(roi_df, use_container_width=True, hide_index=True)


def render_ai_recommendations(df):
    """Render AI recommendations tab"""

    if st.session_state.recommendations is None:
        engine = AIRecommendationEngine(df)
        st.session_state.recommendations = engine.analyze_and_generate_recommendations()

    recs = st.session_state.recommendations

    critical_count = len([r for r in recs if r.priority == RecommendationPriority.CRITICAL])
    high_count = len([r for r in recs if r.priority == RecommendationPriority.HIGH])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E74C3C, #C0392B); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 2rem;">🔴</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{critical_count}</div>
            <div style="font-size: 0.8rem;">Critical Priority</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E67E22, #D35400); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 2rem;">🟠</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{high_count}</div>
            <div style="font-size: 0.8rem;">High Priority</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F4C75, #1B262C); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 2rem;">📋</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{len(recs)}</div>
            <div style="font-size: 0.8rem;">Total Recommendations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    for i, rec in enumerate(recs):
        color = {'CRITICAL': '#E74C3C', 'HIGH': '#E67E22', 'MEDIUM': '#F1C40F', 'LOW': '#2ECC71'}.get(rec.priority.value, '#95A5A6')

        with st.expander(f"[{rec.priority.value}] {rec.title} - {rec.asset_name}", expanded=(i < 3)):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Category:** {rec.category}")
                st.write(rec.description)
            with col2:
                st.metric("Effort", f"{rec.estimated_effort_days} days")
            st.markdown("**Actions:**")
            for action in rec.actions:
                st.markdown(f"- {action}")
            st.warning(f"**Risk if Ignored:** {rec.risk_if_ignored}")


def render_file_upload():
    """Render file upload tab for Excel/CSV files"""
    
    st.subheader("📁 Upload Asset Inventory")
    
    st.markdown("""
    <div class="info-box">
    <strong>Supported Formats:</strong> Excel (.xlsx, .xls), CSV (.csv)
    <br/><br/>
    <strong>Required Columns:</strong><br/>
    • Asset Name<br/>
    • Algorithm<br/>
    • Key Size<br/>
    • Usage Area<br/>
    • Data Sensitivity<br/>
    • Data Volume (GB)
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your asset inventory file",
        type=['xlsx', 'xls', 'csv'],
        help="Upload your cryptographic asset inventory for analysis"
    )
    
    if uploaded_file is not None:
        try:
            file_bytes = uploaded_file.getvalue()
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            with st.spinner(f"Processing {uploaded_file.name}..."):
                success, assets, error = FileParser.parse_file(file_bytes, file_extension)
            
            if success:
                st.success(f"✅ Successfully loaded {len(assets)} assets from {uploaded_file.name}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Assets Imported", len(assets))
                with col2:
                    st.metric("File Type", file_extension.upper())
                
                preview = pd.DataFrame([{
                    "Asset Name": a.name,
                    "Algorithm": a.algorithm.value,
                    "Key Size": a.key_size,
                    "Usage Area": a.usage_area,
                    "Sensitivity": a.data_sensitivity,
                    "Data Volume (GB)": a.estimated_data_volume_gb
                } for a in assets])
                
                st.subheader("Preview of Imported Data")
                st.dataframe(preview, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🚀 Use Uploaded Data for Analysis", use_container_width=True):
                        st.session_state.uploaded_assets = assets
                        st.session_state.uploaded_file_name = uploaded_file.name
                        st.session_state.use_uploaded_data = True
                        st.session_state.recommendations = None
                        st.success("Data ready! Go to the Dashboard tab to view analysis.")
                
                with col2:
                    if st.button("🗑️ Clear Upload", use_container_width=True):
                        st.session_state.uploaded_assets = None
                        st.session_state.uploaded_file_name = None
                        st.session_state.use_uploaded_data = False
                        st.session_state.recommendations = None
                        st.rerun()
            else:
                st.error(f"❌ Error: {error}")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    if st.session_state.uploaded_assets is not None:
        st.markdown("---")
        st.success(f"📊 Current data source: {st.session_state.uploaded_file_name}")


def render_asset_management():
    """Render asset management tab"""

    st.subheader("Add New Asset")

    col1, col2 = st.columns(2)

    with col1:
        asset_name = st.text_input("Asset Name")
        algorithm = st.selectbox("Algorithm", [a.value for a in CryptoAlgorithm])
        usage_area = st.selectbox("Usage Area", ["Core Banking", "Payment Processing", "Customer Authentication", "Data Storage", "API Security", "Mobile Banking", "ATM Network"])

    with col2:
        key_size = st.number_input("Key Size (bits)", value=2048)
        data_sensitivity = st.selectbox("Sensitivity", ["Critical", "High", "Medium", "Low"])
        data_volume = st.number_input("Data Volume (GB)", value=100)

    if st.button("➕ Add Asset"):
        if asset_name:
            st.session_state.custom_assets.append({
                "name": asset_name,
                "algorithm": algorithm,
                "key_size": key_size,
                "usage_area": usage_area,
                "data_sensitivity": data_sensitivity,
                "data_volume": data_volume
            })
            st.success(f"Added: {asset_name}")
            st.rerun()

    if st.session_state.custom_assets:
        st.subheader("Custom Assets")
        st.dataframe(pd.DataFrame(st.session_state.custom_assets), use_container_width=True)
        if st.button("🗑️ Clear All"):
            st.session_state.custom_assets = []
            st.rerun()


def render_reports(df, config):
    """Render reports tab"""

    st.subheader("Download Reports")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📋 **Executive Summary**\n\nFor board and C-suite")
        if st.button("Download Executive Report", use_container_width=True):
            report = f"""# Executive Summary\n\nBank: {config['bank_name']}\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\n## Key Findings\n- Total Assets: {len(df)}\n- Critical: {len(df[df['Threat Level']=='CRITICAL'])}\n- High Risk: {len(df[df['Threat Level']=='HIGH'])}\n- Total Cost: ${df['Est. Migration Cost ($)'].sum()/1e6:.2f}M"""
            st.download_button("📥 Download", report, "executive_report.md", "text/markdown")

    with col2:
        st.success("🔧 **Technical Report**\n\nFor IT and security teams")
        csv = df.to_csv(index=False)
        st.download_button("📥 Download", csv, "technical_report.csv", "text/csv", use_container_width=True)

    with col3:
        st.warning("📜 **Compliance Report**\n\nRegulatory gap analysis")
        checker = QuantumComplianceChecker(bank_size=config["bank_size"], quantum_readiness_level=config["quantum_readiness"])
        compliance_csv = checker.generate_compliance_report().to_csv(index=False)
        st.download_button("📥 Download", compliance_csv, "compliance_report.csv", "text/csv", use_container_width=True)


def main():
    """Main application"""

    init_session_state()
    config = render_sidebar()
    st.session_state.config = config

    # Header
    st.markdown('<h1 class="main-header">Quantum Computing Risk Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Enterprise cryptographic vulnerability assessment with AI-powered insights</p>', unsafe_allow_html=True)

    # Get assets
    if st.session_state.use_uploaded_data and st.session_state.uploaded_assets is not None:
        assets = st.session_state.uploaded_assets
        st.info(f"📊 Using uploaded data from: {st.session_state.uploaded_file_name}")
    elif config["use_sample_data"]:
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
            st.info("Enable 'Use Sample Data' or add assets in Asset Management or File Upload tab")
            render_file_upload()
            render_asset_management()
            return

    # Generate risk data
    risk_data = generate_risk_report(assets, config["quantum_advancement"])
    st.session_state.risk_data = risk_data

    # Dashboard
    render_dashboard(risk_data, config)

    st.markdown("---")

    # Main tabs
    tabs = st.tabs([
        "📊 Risk Analysis", 
        "📁 Upload", 
        "📜 Compliance", 
        "💰 Cost Analysis", 
        "🤖 AI Recommendations", 
        "🏦 Assets", 
        "📋 Reports"
    ])

    with tabs[0]:
        render_risk_analysis(risk_data)

    with tabs[1]:
        render_file_upload()

    with tabs[2]:
        render_compliance(config)

    with tabs[3]:
        render_cost_analysis(risk_data, config)

    with tabs[4]:
        render_ai_recommendations(risk_data)

    with tabs[5]:
        render_asset_management()

    with tabs[6]:
        render_reports(risk_data, config)

    # Footer
    st.markdown("""
    <div class="footer">
        Quantum Risk Analyzer v2.0 | Built for Banking Security
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
