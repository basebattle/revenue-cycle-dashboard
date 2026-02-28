import streamlit as st
import os
from revenue_cycle_dashboard.config.settings import settings

def main():
    st.set_page_config(
        page_title=settings.app_name,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 1. Sidebar Logo and Nav
    st.sidebar.title("🏥 RevCycle Intel")
    st.sidebar.markdown("---")
    
    # 2. Page Selection
    page = st.sidebar.radio(
        "Navigation",
        ["📈 Dashboard", "💬 AI Query", "📋 Reports", "⚖️ Benchmarks", "⚙️ Data Management"],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.caption(f"v1.0.0 | {os.name.upper()} | Feb 2026")

    # 3. Routing Logic
    if page == "📈 Dashboard":
        from revenue_cycle_dashboard.views.dashboard import render
        render()
    elif page == "💬 AI Query":
        from revenue_cycle_dashboard.views.query import render
        render()
    elif page == "📋 Reports":
        from revenue_cycle_dashboard.views.reports import render
        render()
    elif page == "⚖️ Benchmarks":
        from revenue_cycle_dashboard.views.benchmarks import render
        render()
    elif page == "⚙️ Data Management":
        from revenue_cycle_dashboard.views.data_management import render
        render()


if __name__ == "__main__":
    main()
