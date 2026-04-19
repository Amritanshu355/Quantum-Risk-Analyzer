"""
Enhanced Dashboard Components for Quantum Risk Analyzer
Modern, resume-worthy UI components with animations and interactivity
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple


def create_modern_metric_card(label: str, value: str, delta: str = None,
                               delta_type: str = "normal", icon: str = "📊") -> str:
    """Create a modern metric card with icon and styling"""

    color_map = {
        "normal": "#667eea",
        "positive": "#27AE60",
        "negative": "#E74C3C",
        "warning": "#F39C12"
    }

    delta_color = color_map.get(delta_type, color_map["normal"])
    delta_html = f"""
    <div style="font-size: 0.9rem; color: {delta_color}; margin-top: 0.3rem;">
        {'↑' if delta_type == 'positive' else '↓' if delta_type == 'negative' else ''} {delta}
    </div>""" if delta else ""

    return f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: transform 0.3s ease;
    "
    onmouseover="this.style.transform='translateY(-5px)'"
    onmouseout="this.style.transform='translateY(0)'">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">
            {label}
        </div>
        <div style="font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0;">{value}</div>
        {delta_html}
    </div>
    """


def create_animated_risk_gauge(risk_data: pd.DataFrame) -> go.Figure:
    """Create an animated gauge showing overall risk posture"""

    critical_pct = len(risk_data[risk_data['Threat Level'] == 'CRITICAL']) / len(risk_data) * 100
    high_pct = len(risk_data[risk_data['Threat Level'] == 'HIGH']) / len(risk_data) * 100
    avg_vuln = risk_data['Vulnerability Score'].mean()

    overall_risk = min(100, (critical_pct * 2 + high_pct + avg_vuln) / 3)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall_risk,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Overall Risk Posture</b>", 'font': {'size': 16, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "white", 'tickwidth': 2},
            'bar': {'color': "white"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 20], 'color': '#27AE60'},
                {'range': [20, 40], 'color': '#2ECC71'},
                {'range': [40, 60], 'color': '#F1C40F'},
                {'range': [60, 80], 'color': '#E67E22'},
                {'range': [80, 100], 'color': '#E74C3C'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Inter, sans-serif"}
    )

    return fig


def create_3d_risk_surface(risk_data: pd.DataFrame) -> go.Figure:
    """Create an interactive 3D risk surface visualization"""

    # Create a grid of vulnerability vs timeline
    vuln_range = np.linspace(0, 100, 30)
    timeline_range = np.linspace(1, 30, 30)
    V, T = np.meshgrid(vuln_range, timeline_range)

    # Risk = Vulnerability * (10 / Timeline)
    Z = V * (10 / T)

    # Normalize to 0-100
    Z = np.clip(Z, 0, 100)

    fig = go.Figure(data=[go.Surface(
        x=V,
        y=T,
        z=Z,
        colorscale='RdYlGn_r',
        opacity=0.9,
        hovertemplate="Vulnerability: %{x:.1f}%<br>Timeline: %{y:.1f} yrs<br>Risk: %{z:.1f}<extra></extra>"
    )])

    # Add actual data points as scatter markers
    fig.add_trace(go.Scatter3d(
        x=risk_data['Vulnerability Score'],
        y=risk_data['Years to Threat'],
        z=risk_data['Vulnerability Score'] * (10 / risk_data['Years to Threat']),
        mode='markers',
        marker=dict(
            size=6,
            color=risk_data['Migration Priority'],
            colorscale='Viridis',
            opacity=1,
            colorbar=dict(title="Priority")
        ),
        text=risk_data['Asset Name'],
        hovertemplate="<b>%{text}</b><br>Vuln: %{x:.1f}%<br>Timeline: %{y:.1f} yrs<extra></extra>"
    ))

    fig.update_layout(
        title="<b>3D Risk Surface Analysis</b>",
        scene=dict(
            xaxis_title="Vulnerability Score (%)",
            yaxis_title="Years to Threat",
            zaxis_title="Risk Score",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig


def create_risk_sunburst(risk_data: pd.DataFrame) -> go.Figure:
    """Create a sunburst chart showing risk distribution by usage area and threat level"""

    # Aggregate data for sunburst
    sunburst_data = risk_data.groupby(['Usage Area', 'Threat Level']).size().reset_index(name='count')
    sunburst_data['percentage'] = sunburst_data['count'] / sunburst_data['count'].sum() * 100

    fig = go.Figure(go.Sunburst(
        labels=sunburst_data.apply(lambda x: f"{x['Usage Area']}<br>{x['Threat Level']}", axis=1).tolist(),
        parents=[''] * len(sunburst_data),
        values=sunburst_data['count'],
        branchvalues="total",
        marker=dict(
            colors=sunburst_data['percentage'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="% of Total")
        ),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
    ))

    fig.update_layout(
        title="<b>Risk Distribution Sunburst</b>",
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig


def create_timeline_forecast(risk_data: pd.DataFrame, advancement_factor: float) -> go.Figure:
    """Create a timeline forecast showing when assets will be at risk"""

    # Create year-by-year risk projection
    years = list(range(1, 16))
    at_risk = []
    cumulative_cost = []

    for year in years:
        assets_at_risk = risk_data[risk_data['Years to Threat'] <= year]
        at_risk.append(len(assets_at_risk))
        cumulative_cost.append(assets_at_risk['Est. Migration Cost ($)'].sum())

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=years,
            y=at_risk,
            name="Assets at Risk",
            line=dict(color='#E74C3C', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Bar(
            x=years,
            y=cumulative_cost,
            name="Cumulative Cost",
            marker_color='#667eea',
            opacity=0.5
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="<b>Quantum Threat Forecast (15-Year Projection)</b>",
        xaxis_title="Years from Now",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxes(title_text="Assets at Risk", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Migration Cost ($)", secondary_y=True)

    return fig


def create_crypto_agility_score(risk_data: pd.DataFrame) -> go.Figure:
    """Create a radar chart showing crypto-agility readiness across dimensions"""

    # Calculate scores for different dimensions
    algo_diversity = len(risk_data['Algorithm'].unique()) / 10 * 100
    avg_migration_priority = (100 - risk_data['Migration Priority'].mean())
    low_vuln_pct = len(risk_data[risk_data['Vulnerability Score'] < 50]) / len(risk_data) * 100
    long_timeline_pct = len(risk_data[risk_data['Years to Threat'] > 10]) / len(risk_data) * 100
    low_cost_pct = len(risk_data[risk_data['Est. Migration Cost ($)'] < 300000]) / len(risk_data) * 100

    categories = ['Algorithm<br>Diversity', 'Migration<br>Readiness', 'Low<br>Vulnerability',
                  'Time<br>Buffer', 'Cost<br>Affordability']

    values = [algo_diversity, avg_migration_priority, low_vuln_pct, long_timeline_pct, low_cost_pct]
    values = values + [values[0]]  # Close the radar
    categories = categories + [categories[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.5)',
        line=dict(color='#667eea', width=3),
        name='Crypto-Agility Score'
    ))

    overall_score = np.mean(values[:-1])

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickcolor="white"
            ),
            bgcolor="rgba(0,0,0,0.2)"
        ),
        title=f"<b>Crypto-Agility Score: {overall_score:.1f}/100</b>",
        height=450,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def create_migration_roadmap(risk_data: pd.DataFrame) -> go.Figure:
    """Create a visual migration roadmap with phases"""

    # Categorize assets into migration phases
    phase1 = risk_data[risk_data['Years to Threat'] <= 5]  # Immediate
    phase2 = risk_data[(risk_data['Years to Threat'] > 5) & (risk_data['Years to Threat'] <= 10)]  # Short-term
    phase3 = risk_data[(risk_data['Years to Threat'] > 10) & (risk_data['Years to Threat'] <= 15)]  # Medium-term
    phase4 = risk_data[risk_data['Years to Threat'] > 15]  # Long-term

    phases = [
        {"name": "Phase 1: Immediate", "assets": phase1, "color": "#E74C3C", "timeline": "0-18 months"},
        {"name": "Phase 2: Short-term", "assets": phase2, "color": "#E67E22", "timeline": "18-36 months"},
        {"name": "Phase 3: Medium-term", "assets": phase3, "color": "#F1C40F", "timeline": "36-60 months"},
        {"name": "Phase 4: Long-term", "assets": phase4, "color": "#27AE60", "timeline": "60+ months"}
    ]

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[f"{p['name']} ({len(p['assets'])} assets)" for p in phases],
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]]
    )

    for i, phase in enumerate(phases):
        row = (i // 2) + 1
        col = (i % 2) + 1

        if len(phase['assets']) > 0:
            df = phase['assets']
            fig.add_trace(
                go.Bar(
                    x=df['Asset Name'],
                    y=df['Vulnerability Score'],
                    marker_color=phase['color'],
                    name=phase['name'],
                    showlegend=False
                ),
                row=row, col=col
            )

    fig.update_layout(
        title="<b>Migration Roadmap by Phase</b>",
        height=600,
        showlegend=False
    )

    fig.update_xaxes(tickangle=-45)
    fig.update_yaxes(title_text="Vulnerability Score")

    return fig


def create_ai_recommendation_card(asset_name: str, threat_level: str,
                                   vulnerability: float, recommendations: List[str]) -> str:
    """Create a styled AI recommendation card"""

    colors = {
        'CRITICAL': '#E74C3C',
        'HIGH': '#E67E22',
        'MEDIUM': '#F1C40F',
        'LOW': '#2ECC71',
        'MINIMAL': '#3498DB'
    }

    color = colors.get(threat_level, '#95A5A6')

    rec_items = ''.join([f'<li style="margin: 0.5rem 0; padding-left: 0.5rem;">{rec}</li>'
                         for rec in recommendations[:3]])

    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid {color};
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h4 style="margin: 0; color: {color};">🤖 AI Recommendation: {asset_name}</h4>
            <span style="
                background: {color};
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: bold;
            ">{threat_level}</span>
        </div>
        <p style="margin: 0.5rem 0; color: #666;">
            Vulnerability Score: <strong>{vulnerability:.1f}%</strong>
        </p>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem; color: #444;">
            {rec_items}
        </ul>
    </div>
    """


def create_status_badge(status: str) -> str:
    """Create a status badge HTML element"""

    colors = {
        'secure': '#27AE60',
        'warning': '#F1C40F',
        'critical': '#E74C3C',
        'info': '#3498DB'
    }

    icons = {
        'secure': '✓',
        'warning': '⚠',
        'critical': '✕',
        'info': 'ℹ'
    }

    color = colors.get(status, '#95A5A6')
    icon = icons.get(status, '•')

    return f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: {color}20;
        color: {color};
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    ">
        {icon} {status.upper()}
    </span>
    """
