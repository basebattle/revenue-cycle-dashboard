import streamlit as st
from typing import Literal

def render_anomaly_alert(
    severity: Literal["critical", "warning", "info"],
    message: str,
    metric: str
):
    """Renders an alert banner for a detected anomaly."""
    
    # 1. Icons and colors
    icon_map = {
        'critical': '🔴',
        'warning': '🟠',
        'info': '🔵'
    }
    color_map = {
        'critical': '#FEE2E2', # Red-50
        'warning': '#FEF3C7', # Amber-50
        'info': '#DBEAFE' # Blue-50
    }
    border_map = {
        'critical': '#EF4444', # Red-500
        'warning': '#F59E0B', # Amber-500
        'info': '#3B82F6' # Blue-500
    }
    
    icon = icon_map.get(severity, '⚪')
    color = color_map.get(severity, '#F9FAFB')
    border = border_map.get(severity, '#E5E7EB')
    
    # 2. Render HTML
    st.markdown(f"""
        <div style='
            background-color: {color};
            border-left: 4px solid {border};
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        '>
            <span style='margin-right: 12px;'>{icon}</span>
            <div>
                <span style='font-weight: bold;'>{metric}:</span> {message}
            </div>
        </div>
    """, unsafe_allow_html=True)
