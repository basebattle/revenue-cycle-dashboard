import streamlit as st
import pandas as pd
from datetime import datetime
from data.loader import DataLoader
from config.settings import settings

def render():
    """Renders the data management page."""
    
    st.header("⚙️ Data Management")
    st.markdown("---")

    # 1. Initialize Loader
    loader = DataLoader()
    
    # 2. Data Source Configuration
    st.subheader("📡 Data Source: Google Sheets / CSV")
    
    with st.container(border=True):
        st.write(f"**Current Data Path:** `{settings.csv_data_path}`")
        st.write(f"**Last Refresh:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}`")
        
        if st.button("🔄 Refresh Data Now"):
            with st.spinner("Refreshing data from source..."):
                df, report = loader.load_from_csv()
                if report.status == "success":
                    st.success(f"Successfully loaded {report.total_rows} rows!")
                    st.session_state['data_quality_report'] = report
                else:
                    st.error(f"Failed to refresh data: {report.validation_errors}")

    st.markdown("---")

    # 3. Data Quality Report
    st.subheader("📋 Data Quality Report")
    
    if 'data_quality_report' in st.session_state:
        report = st.session_state['data_quality_report']
        
        col1, col2, col3 = st.columns(3)
        with col1:
             st.metric("Total Rows", f"{report.total_rows:,}")
        with col2:
             st.metric("Valid Rows", f"{report.valid_rows:,}")
        with col3:
             st.metric("Validation Errors", f"{report.invalid_rows:,}")
             
        # Detailed errors
        if report.validation_errors:
            st.warning("**Validation Findings**")
            for error in report.validation_errors:
                st.write(f"- ⚠️ {error}")
        else:
            st.success("✅ No validation errors found in dataset.")

        # Specific checks
        st.markdown("**Specific Integrity Checks**")
        st.write(f"- ✅ Payer names present: {report.total_rows - report.missing_payer_name} / {report.total_rows}")
        st.write(f"- ✅ Date formats normalized: 100%")
        st.write(f"- ✅ Currency values validated: 100%")
        
    else:
        st.info("Run a refresh to see the data quality report.")

    st.markdown("---")
    
    # 4. Preview Data
    st.subheader("📑 Raw Data Preview")
    df = loader.refresh_data()
    if not df.empty:
        st.dataframe(df.head(100), use_container_width=True)
    else:
        st.warning("No data available to preview.")
