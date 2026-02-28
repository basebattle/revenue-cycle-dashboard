import streamlit as st
from datetime import datetime

def render_chat_message(role: str, content: str, timestamp: str = None):
    """Renders a chat message bubble in Streamlit."""
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
        
    if role == "user":
        bg_color = "#E5E7EB" # Gray-200
        align = "flex-end"
        text_align = "right"
        avatar = "👤"
    else:
        bg_color = "#DBEAFE" # Blue-100
        align = "flex-start"
        text_align = "left"
        avatar = "🤖"

    st.markdown(f"""
        <div style='display: flex; flex-direction: column; align-items: {align}; margin-bottom: 16px;'>
            <div style='display: flex; align-items: center; margin-bottom: 4px;'>
                <span style='font-size: 1.2rem; margin-right: 8px;'>{avatar if role == "agent" else ""}</span>
                <span style='font-size: 0.75rem; color: #6B7280;'>{timestamp}</span>
                <span style='font-size: 1.2rem; margin-left: 8px;'>{avatar if role == "user" else ""}</span>
            </div>
            <div style='
                background-color: {bg_color};
                padding: 12px 16px;
                border-radius: 12px;
                max-width: 80%;
                color: #111827;
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                text-align: {text_align};
            '>
                {content}
            </div>
        </div>
    """, unsafe_allow_html=True)
