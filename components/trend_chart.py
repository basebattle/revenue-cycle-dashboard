import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Literal

def render_trend_chart(
    title: str,
    data: Dict[str, Any], # {"months": [...], "series": [{"name": ..., "values": [...]}]}
    chart_type: Literal["line", "bar", "area", "waterfall", "horizontal_bar"] = "line",
    height: int = 400,
    show_legend: bool = True
):
    """Renders a styled Plotly trend chart in Streamlit."""
    
    fig = go.Figure()

    # 1. Add Trace based on chart_type
    for series in data.get('series', []):
        if chart_type == "line":
            fig.add_trace(go.Scatter(
                x=data.get('months', []),
                y=series.get('values', []),
                name=series.get('name', ''),
                mode='lines+markers',
                line=dict(width=3)
            ))
        elif chart_type == "bar":
            fig.add_trace(go.Bar(
                x=data.get('months', []),
                y=series.get('values', []),
                name=series.get('name', '')
            ))
        elif chart_type == "area":
            fig.add_trace(go.Scatter(
                x=data.get('months', []),
                y=series.get('values', []),
                name=series.get('name', ''),
                mode='lines',
                fill='tozeroy'
            ))
        elif chart_type == "horizontal_bar":
             fig.add_trace(go.Bar(
                x=series.get('values', []),
                y=data.get('months', []),
                name=series.get('name', ''),
                orientation='h'
            ))

    # 2. Add Layout
    fig.update_layout(
         title=title,
         height=height,
         showlegend=show_legend,
         # legend=dict(yanchor="bottom", y=1.02, xanchor="right", x=1, orientation="h")
    )

    # Use Streamlit's plotly rendering
    st.plotly_chart(fig, use_container_width=True)
