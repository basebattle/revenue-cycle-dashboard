import streamlit as st
from datetime import date, timedelta
from typing import List, Tuple, Dict, Any

def render_dashboard_filters(
    available_payers: List[str],
    available_facilities: List[str]
) -> Dict[str, Any]:
    """Renders dashboard filters in the sidebar and returns selected values."""
    
    st.sidebar.markdown("### 🔍 Filters")
    
    # 1. Date Range
    st.sidebar.markdown("**Date Period**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("From", date.today() - timedelta(days=365))
    with col2:
        end_date = st.date_input("To", date.today())
        
    preset_btn = st.sidebar.selectbox("Quick Range", ["Custom", "Last 30 Days", "Last 90 Days", "MTD", "QTD", "YTD", "Last 12 Months"])
    
    # 2. Payer
    st.sidebar.markdown("**Payer Coverage**")
    selected_payers = st.sidebar.multiselect("Select Payers", available_payers, default=available_payers)
    
    # 3. Facility
    st.sidebar.markdown("**Facility Selection**")
    selected_facilities = st.sidebar.multiselect("Select Facilities", available_facilities, default=available_facilities)

    return {
        'start_date': start_date,
        'end_date': end_date,
        'payers': selected_payers,
        'facilities': selected_facilities
    }

def apply_presets(selected: str) -> Tuple[date, date]:
    """Returns start and end dates based on preset selection."""
    today = date.today()
    if selected == "Last 30 Days":
        return today - timedelta(days=30), today
    elif selected == "Last 90 Days":
        return today - timedelta(days=90), today
    elif selected == "MTD":
        return today.replace(day=1), today
    elif selected == "QTD":
        # Simplified: Use 1st Jan, Apr, Jul, Oct
        q = (today.month - 1) // 3
        return date(today.year, 3 * q + 1, 1), today
    elif selected == "YTD":
        return date(today.year, 1, 1), today
    elif selected == "Last 12 Months":
        return today - timedelta(days=365), today
    return None, None
