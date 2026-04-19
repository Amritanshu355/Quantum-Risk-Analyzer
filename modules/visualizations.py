import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List


def apply_light_theme(fig: go.Figure) -> go.Figure:
    """Apply clean white theme with perfect readability"""
    white_bg = "#ffffff"
    light_secondary_bg = "#f6f8fa"
    text_color = "#1f2328"
    accent_color = "#0969da"
    
    fig.update_layout(
        paper_bgcolor=white_bg,
        plot_bgcolor=light_secondary_bg,
        font=dict(color=text_color, size=12),
        title_font=dict(color=text_color, size=16),
        xaxis=dict(
            tickfont=dict(color="#57606a"),
            title_font=dict(color=text_color),
            gridcolor="#d0d7de"
        ),
        yaxis=dict(
            tickfont=dict(color="#57606a"),
            title_font=dict(color=text_color),
            gridcolor="#d0d7de"
        ),
        legend=dict(
            bgcolor=light_secondary_bg,
            font=dict(color=text_color),
            bordercolor="#d0d7de"
        )
    )
    return fig


def create_risk_heatmap(risk_data: pd.DataFrame) -> go.Figure:
    pivot_data = risk_data.pivot_table(
        values='Vulnerability Score',
        index='Usage Area',
        columns='Algorithm',
        aggfunc='mean',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns.tolist(),
        y=pivot_data.index.tolist(),
        colorscale=[
            [0, '#f6f8fa'],
            [0.25, '#c9d1d9'],
            [0.5, '#8b949e'],
            [0.75, '#539bf5'],
            [1, '#0969da']
        ],
        colorbar=dict(title="Risk Score", tickfont=dict(color="#57606a")),
        hoverongaps=False,
        hovertemplate="Algorithm: %{x}<br>Usage Area: %{y}<br>Risk Score: %{z:.1f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Quantum Vulnerability Risk Heatmap",
        xaxis_title="Cryptographic Algorithm",
        yaxis_title="Usage Area",
        height=500
    )
    
    return apply_light_theme(fig)


def create_threat_timeline_chart(risk_data: pd.DataFrame) -> go.Figure:
    df = risk_data.sort_values('Years to Threat')
    
    colors = {
        'CRITICAL': '#cf222e',
        'HIGH': '#9a6700',
        'MEDIUM': '#d4a72c',
        'LOW': '#1a7f37',
        'MINIMAL': '#0969da'
    }
    
    bar_colors = [colors.get(level, '#57606a') for level in df['Threat Level']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['Asset Name'],
            y=df['Years to Threat'],
            marker_color=bar_colors,
            text=df['Years to Threat'].round(1),
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Years to Threat: %{y:.1f}<br>Algorithm: %{customdata[0]}<extra></extra>",
            customdata=df[['Algorithm']].values
        )
    ])
    
    fig.add_hline(y=5, line_dash="dash", line_color="#cf222e", 
                  annotation_text="Critical Threshold (5 years)",
                  annotation_font=dict(color="#57606a"))
    fig.add_hline(y=10, line_dash="dash", line_color="#9a6700",
                  annotation_text="Planning Horizon (10 years)",
                  annotation_font=dict(color="#57606a"))
    
    fig.update_layout(
        title="Quantum Threat Timeline by Asset",
        xaxis_title="Asset",
        yaxis_title="Years Until Quantum Threat",
        xaxis_tickangle=-45,
        height=500,
        showlegend=False
    )
    
    return apply_light_theme(fig)


def create_migration_priority_chart(risk_data: pd.DataFrame) -> go.Figure:
    df = risk_data.sort_values('Migration Priority', ascending=True)
    
    colors = {
        'CRITICAL': '#cf222e',
        'HIGH': '#9a6700',
        'MEDIUM': '#d4a72c',
        'LOW': '#1a7f37',
        'MINIMAL': '#0969da'
    }
    
    bar_colors = [colors.get(level, '#57606a') for level in df['Threat Level']]
    
    fig = go.Figure(data=[
        go.Bar(
            y=df['Asset Name'],
            x=df['Migration Priority'],
            orientation='h',
            marker_color=bar_colors,
            text=df['Migration Priority'],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Priority Score: %{x}<br>Threat Level: %{customdata[0]}<extra></extra>",
            customdata=df[['Threat Level']].values
        )
    ])
    
    fig.update_layout(
        title="Migration Priority Ranking",
        xaxis_title="Priority Score (Higher = More Urgent)",
        yaxis_title="Asset",
        height=500
    )
    
    return apply_light_theme(fig)


def create_cost_breakdown_chart(cost_breakdown: Dict[str, float]) -> go.Figure:
    labels = list(cost_breakdown.keys())
    values = list(cost_breakdown.values())
    
    colors = [
        '#0969da', '#8250df', '#a371f7', '#c96195',
        '#f85149', '#db6d28', '#d29922', '#1a7f37'
    ]
    colors = colors[:len(labels)]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent',
        textfont=dict(color='#1f2328'),
        hovertemplate="<b>%{label}</b><br>Cost: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>"
    )])
    
    total = sum(values)
    fig.add_annotation(
        text=f"Total<br>${total:,.0f}",
        x=0.5, y=0.5,
        font=dict(size=16, color='#1f2328'),
        showarrow=False
    )
    
    fig.update_layout(
        title="Migration Cost Breakdown",
        height=500
    )
    
    return apply_light_theme(fig)


def create_timeline_gantt_chart(timeline_df: pd.DataFrame) -> go.Figure:
    colors = [
        '#0969da', '#8250df', '#a371f7', '#c96195',
        '#f85149', '#db6d28'
    ]
    colors = colors[:len(timeline_df)]
    
    fig = go.Figure()
    
    for i, row in timeline_df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Duration (Months)']],
            y=[row['Phase']],
            orientation='h',
            base=[row['Start Month'] - 1],
            marker_color=colors[i % len(colors)],
            text=f"{row['Duration (Months)']} months",
            textposition='inside',
            name=row['Phase'],
            hovertemplate=f"<b>{row['Phase']}</b><br>Duration: {row['Duration (Months)']} months<br>Cost: ${row['Phase Cost ($)']:,.0f}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Migration Timeline (Gantt Chart)",
        xaxis_title="Months",
        yaxis_title="Phase",
        barmode='stack',
        height=400,
        showlegend=False
    )
    
    return apply_light_theme(fig)


def create_roi_chart(roi_df: pd.DataFrame, total_cost: float) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=roi_df['Year'],
            y=roi_df['Cumulative Savings ($)'],
            name='Cumulative Savings',
            marker_color='#0969da',
            opacity=0.8
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=roi_df['Year'],
            y=roi_df['ROI (%)'],
            name='ROI %',
            line=dict(color='#cf222e', width=3),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    fig.add_hline(y=total_cost, line_dash="dash", line_color="#1a7f37",
                  annotation_text=f"Investment: ${total_cost:,.0f}",
                  annotation_font=dict(color="#57606a"))
    
    breakeven_year = roi_df[roi_df['Net Benefit ($)'] >= 0]['Year'].min()
    if pd.notna(breakeven_year):
        fig.add_vline(x=breakeven_year, line_dash="dash", line_color="#8250df",
                      annotation_text=f"Breakeven: Year {breakeven_year}",
                      annotation_font=dict(color="#57606a"))
    
    fig.update_layout(
        title="Return on Investment Analysis",
        xaxis_title="Year",
        height=500
    )
    
    fig.update_yaxes(title_text="Cumulative Savings ($)", secondary_y=False, title_font=dict(color="#1f2328"), tickfont=dict(color="#57606a"))
    fig.update_yaxes(title_text="ROI (%)", secondary_y=True, title_font=dict(color="#1f2328"), tickfont=dict(color="#57606a"))
    
    return apply_light_theme(fig)


def create_compliance_gauge(score: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Compliance Score", 'font': {'size': 24, 'color': "#1f2328"}},
        delta={'reference': 70, 'increasing': {'color': "#1a7f37"}, 'decreasing': {'color': "#cf222e"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#57606a"},
            'bar': {'color': "#0969da"},
            'bgcolor': "#f6f8fa",
            'borderwidth': 2,
            'bordercolor': "#d0d7de",
            'steps': [
                {'range': [0, 30], 'color': '#cf222e'},
                {'range': [30, 50], 'color': '#9a6700'},
                {'range': [50, 70], 'color': '#d4a72c'},
                {'range': [70, 85], 'color': '#1a7f37'},
                {'range': [85, 100], 'color': '#1a7f37'}
            ],
            'threshold': {
                'line': {'color': "#cf222e", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        paper_bgcolor="#ffffff"
    )
    
    return fig


def create_algorithm_vulnerability_radar(risk_data: pd.DataFrame) -> go.Figure:
    algo_scores = risk_data.groupby('Algorithm')['Vulnerability Score'].mean().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=algo_scores['Vulnerability Score'].tolist() + [algo_scores['Vulnerability Score'].iloc[0]],
        theta=algo_scores['Algorithm'].tolist() + [algo_scores['Algorithm'].iloc[0]],
        fill='toself',
        fillcolor='rgba(9, 105, 218, 0.3)',
        line=dict(color='#0969da', width=2),
        name='Vulnerability Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#57606a")
            ),
            angularaxis=dict(
                tickfont=dict(color="#57606a")
            ),
            bgcolor="#f6f8fa"
        ),
        title="Algorithm Vulnerability Radar",
        height=500
    )
    
    return apply_light_theme(fig)


def create_threat_distribution_pie(risk_data: pd.DataFrame) -> go.Figure:
    threat_counts = risk_data['Threat Level'].value_counts()
    
    colors = {
        'CRITICAL': '#cf222e',
        'HIGH': '#9a6700',
        'MEDIUM': '#d4a72c',
        'LOW': '#1a7f37',
        'MINIMAL': '#0969da'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=threat_counts.index,
        values=threat_counts.values,
        marker_colors=[colors.get(level, '#57606a') for level in threat_counts.index],
        textinfo='label+value+percent',
        textfont=dict(color='#1f2328'),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Threat Level Distribution",
        height=400
    )
    
    return apply_light_theme(fig)


def create_cost_vs_risk_scatter(risk_data: pd.DataFrame) -> go.Figure:
    colors = {
        'CRITICAL': '#cf222e',
        'HIGH': '#9a6700',
        'MEDIUM': '#d4a72c',
        'LOW': '#1a7f37',
        'MINIMAL': '#0969da'
    }
    
    fig = go.Figure()
    
    for threat_level in risk_data['Threat Level'].unique():
        df_filtered = risk_data[risk_data['Threat Level'] == threat_level]
        fig.add_trace(go.Scatter(
            x=df_filtered['Vulnerability Score'],
            y=df_filtered['Est. Migration Cost ($)'],
            mode='markers',
            name=threat_level,
            marker=dict(
                size=df_filtered['Migration Priority'] / 5,
                color=colors.get(threat_level, '#57606a'),
                opacity=0.9
            ),
            text=df_filtered['Asset Name'],
            hovertemplate="<b>%{text}</b><br>Vulnerability: %{x:.1f}<br>Cost: $%{y:,.0f}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Migration Cost vs Vulnerability Score",
        xaxis_title="Vulnerability Score",
        yaxis_title="Estimated Migration Cost ($)",
        height=500
    )
    
    return apply_light_theme(fig)
