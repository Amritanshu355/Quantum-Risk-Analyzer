import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List


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
            [0, '#2ECC71'],
            [0.25, '#F1C40F'],
            [0.5, '#E67E22'],
            [0.75, '#E74C3C'],
            [1, '#8E44AD']
        ],
        colorbar=dict(title="Risk Score"),
        hoverongaps=False,
        hovertemplate="Algorithm: %{x}<br>Usage Area: %{y}<br>Risk Score: %{z:.1f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Quantum Vulnerability Risk Heatmap",
        xaxis_title="Cryptographic Algorithm",
        yaxis_title="Usage Area",
        height=500
    )
    
    return fig


def create_threat_timeline_chart(risk_data: pd.DataFrame) -> go.Figure:
    df = risk_data.sort_values('Years to Threat')
    
    colors = {
        'CRITICAL': '#E74C3C',
        'HIGH': '#E67E22',
        'MEDIUM': '#F1C40F',
        'LOW': '#2ECC71',
        'MINIMAL': '#3498DB'
    }
    
    bar_colors = [colors.get(level, '#95A5A6') for level in df['Threat Level']]
    
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
    
    fig.add_hline(y=5, line_dash="dash", line_color="red", 
                  annotation_text="Critical Threshold (5 years)")
    fig.add_hline(y=10, line_dash="dash", line_color="orange",
                  annotation_text="Planning Horizon (10 years)")
    
    fig.update_layout(
        title="Quantum Threat Timeline by Asset",
        xaxis_title="Asset",
        yaxis_title="Years Until Quantum Threat",
        xaxis_tickangle=-45,
        height=500,
        showlegend=False
    )
    
    return fig


def create_migration_priority_chart(risk_data: pd.DataFrame) -> go.Figure:
    df = risk_data.sort_values('Migration Priority', ascending=True)
    
    colors = {
        'CRITICAL': '#E74C3C',
        'HIGH': '#E67E22',
        'MEDIUM': '#F1C40F',
        'LOW': '#2ECC71',
        'MINIMAL': '#3498DB'
    }
    
    bar_colors = [colors.get(level, '#95A5A6') for level in df['Threat Level']]
    
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
    
    return fig


def create_cost_breakdown_chart(cost_breakdown: Dict[str, float]) -> go.Figure:
    labels = list(cost_breakdown.keys())
    values = list(cost_breakdown.values())
    
    colors = px.colors.qualitative.Set3[:len(labels)]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>Cost: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>"
    )])
    
    total = sum(values)
    fig.add_annotation(
        text=f"Total<br>${total:,.0f}",
        x=0.5, y=0.5,
        font_size=16,
        showarrow=False
    )
    
    fig.update_layout(
        title="Migration Cost Breakdown",
        height=500
    )
    
    return fig


def create_timeline_gantt_chart(timeline_df: pd.DataFrame) -> go.Figure:
    colors = px.colors.qualitative.Pastel[:len(timeline_df)]
    
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
    
    return fig


def create_roi_chart(roi_df: pd.DataFrame, total_cost: float) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=roi_df['Year'],
            y=roi_df['Cumulative Savings ($)'],
            name='Cumulative Savings',
            marker_color='#3498DB',
            opacity=0.7
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=roi_df['Year'],
            y=roi_df['ROI (%)'],
            name='ROI %',
            line=dict(color='#E74C3C', width=3),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    fig.add_hline(y=total_cost, line_dash="dash", line_color="green",
                  annotation_text=f"Investment: ${total_cost:,.0f}")
    
    breakeven_year = roi_df[roi_df['Net Benefit ($)'] >= 0]['Year'].min()
    if pd.notna(breakeven_year):
        fig.add_vline(x=breakeven_year, line_dash="dash", line_color="purple",
                      annotation_text=f"Breakeven: Year {breakeven_year}")
    
    fig.update_layout(
        title="Return on Investment Analysis",
        xaxis_title="Year",
        height=500
    )
    
    fig.update_yaxes(title_text="Cumulative Savings ($)", secondary_y=False)
    fig.update_yaxes(title_text="ROI (%)", secondary_y=True)
    
    return fig


def create_compliance_gauge(score: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Compliance Score", 'font': {'size': 24}},
        delta={'reference': 70, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#E74C3C'},
                {'range': [30, 50], 'color': '#E67E22'},
                {'range': [50, 70], 'color': '#F1C40F'},
                {'range': [70, 85], 'color': '#2ECC71'},
                {'range': [85, 100], 'color': '#27AE60'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=350)
    
    return fig


def create_algorithm_vulnerability_radar(risk_data: pd.DataFrame) -> go.Figure:
    algo_scores = risk_data.groupby('Algorithm')['Vulnerability Score'].mean().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=algo_scores['Vulnerability Score'].tolist() + [algo_scores['Vulnerability Score'].iloc[0]],
        theta=algo_scores['Algorithm'].tolist() + [algo_scores['Algorithm'].iloc[0]],
        fill='toself',
        fillcolor='rgba(231, 76, 60, 0.3)',
        line=dict(color='#E74C3C', width=2),
        name='Vulnerability Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Algorithm Vulnerability Radar",
        height=500
    )
    
    return fig


def create_threat_distribution_pie(risk_data: pd.DataFrame) -> go.Figure:
    threat_counts = risk_data['Threat Level'].value_counts()
    
    colors = {
        'CRITICAL': '#E74C3C',
        'HIGH': '#E67E22',
        'MEDIUM': '#F1C40F',
        'LOW': '#2ECC71',
        'MINIMAL': '#3498DB'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=threat_counts.index,
        values=threat_counts.values,
        marker_colors=[colors.get(level, '#95A5A6') for level in threat_counts.index],
        textinfo='label+value+percent',
        hole=0.3
    )])
    
    fig.update_layout(
        title="Threat Level Distribution",
        height=400
    )
    
    return fig


def create_cost_vs_risk_scatter(risk_data: pd.DataFrame) -> go.Figure:
    colors = {
        'CRITICAL': '#E74C3C',
        'HIGH': '#E67E22',
        'MEDIUM': '#F1C40F',
        'LOW': '#2ECC71',
        'MINIMAL': '#3498DB'
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
                color=colors.get(threat_level, '#95A5A6'),
                opacity=0.7
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
    
    return fig
