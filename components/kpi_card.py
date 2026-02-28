import streamlit as st
import plotly.graph_objects as go
from typing import Optional, List, Literal

def render_kpi_card(
    title: str,
    value: float,
    format_type: Literal["percent", "currency", "days", "ratio"],
    trend_pct: Optional[float] = None,
    trend_direction: Literal["up", "down", "flat"] = "flat",
    is_inverse: bool = False, # True for metrics where lower = better (e.g. Days in A/R)
    sparkline_data: Optional[List[float]] = None,
    benchmark_percentile: Optional[int] = None,
    subtitle: Optional[str] = None
):
    """Renders a styled KPI card in Streamlit."""
    
    # 1. Format value based on type
    if format_type == "percent":
        display_value = f"{value:.1f}%"
    elif format_type == "currency":
        display_value = f"${value:.2f}"
    elif format_type == "days":
        display_value = f"{value:.1f}"
    else:
        display_value = f"{value:.2f}"

    # 2. Determine trend color
    # Improving: Up for pos-metrics, Down for neg-metrics
    color = "gray"
    if trend_direction == "up":
        color = "red" if is_inverse else "green"
        arrow = "▲"
    elif trend_direction == "down":
        color = "green" if is_inverse else "red"
        arrow = "▼"
    else:
        color = "gray"
        arrow = "●"
        
    trend_display = f"<span style='color:{color}; font-weight:bold;'>{arrow} {abs(trend_pct):.1f}%</span>" if trend_pct is not None else ""

    # 3. HTML Layout
    st.markdown(f"""
        <div style='
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid #E5E7EB;
            height: 100%;
        '>
            <div style='color: #6B7280; font-size: 0.875rem; font-weight: 500;'>{title}</div>
            <div style='display: flex; align-items: baseline; margin-top: 8px;'>
                <div style='font-size: 1.875rem; font-weight: 700; color: #111827;'>{display_value}</div>
                <div style='margin-left: 10px; font-size: 0.875rem;'>{trend_display}</div>
            </div>
            {f"<div style='color: #9CA3AF; font-size: 0.75rem; margin-top: 4px;'>{subtitle}</div>" if subtitle else ""}
            {f"<div style='display: inline-block; background-color: #F3F4F6; color: #374151; font-size: 0.75rem; padding: 2px 8px; border-radius: 9999px; margin-top: 8px;'>{benchmark_percentile}th percentile</div>" if benchmark_percentile else ""}
        </div>
    """, unsafe_allow_html=True)

    # 4. Optional Sparkline (drawn below HTML to keep layout clean)
    if sparkline_data:
        # Drawing a minimal sparkline with Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=sparkline_data,
            mode='lines',
            line=dict(color='#85C1E9', width=2),
            fill='tozeroy',
            fillcolor='rgba(133, 193, 233, 0.2)'
        ))
        fig.update_layout(
             margin=dict(l=0, r=0, t=0, b=0),
             height=30,
             width=200,
             xaxis=dict(visible=False),
             yaxis=dict(visible=False),
             showlegend=False,
             plot_bgcolor='rgba(0,0,0,0)',
             paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
