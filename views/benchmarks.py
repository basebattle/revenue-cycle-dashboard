import streamlit as st
import pandas as pd
from revenue_cycle_dashboard.data.loader import DataLoader
from revenue_cycle_dashboard.data.calculator import KPICalculator
from revenue_cycle_dashboard.data.benchmarks import BenchmarkData
from revenue_cycle_dashboard.config.constants import KPI_METADATA

def render():
    st.header("⚖️ Benchmark Comparison")
    st.markdown("---")

    # 1. Profile Config
    st.subheader("🏥 Hospital Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Hospital Type", ["Community", "Academic", "Rural", "Specialty"], index=0)
    with col2:
        st.selectbox("Bed Count", ["1-99", "100-249", "250-499", "500+"], index=1)
    with col3:
        st.selectbox("Region", ["West", "Midwest", "Northeast", "South", "Global"], index=1)

    st.markdown("---")

    # 2. Comparison Table
    st.subheader("🏁 Performance vs. Benchmarks")
    
    loader = DataLoader()
    calculator = KPICalculator()
    benchmarks = BenchmarkData()
    
    df = loader.refresh_data()
    kpis = calculator.calculate_all(df)
    b_data = benchmarks.get_benchmarks()

    # Build Table
    table_rows = []
    for kpi_slug, meta in KPI_METADATA.items():
        actual = kpis.get(kpi_slug, 0)
        b = b_data.get(kpi_slug, {})
        status = benchmarks.get_benchmark_status(kpi_slug, actual)
        
        table_rows.append({
            "Metric": meta['label'],
            "You": f"{actual}%" if meta['format'] == 'percent' else (f"${actual:.2f}" if meta['format'] == 'currency' else str(actual)),
            "50th (Median)": f"{b.get('50th')}%" if meta['format'] == 'percent' else str(b.get('50th')),
            "75th": f"{b.get('75th')}%" if meta['format'] == 'percent' else str(b.get('75th')),
            "90th": f"{b.get('90th')}%" if meta['format'] == 'percent' else str(b.get('90th')),
            "Status": status
        })

    st.table(pd.DataFrame(table_rows))

    # 3. AI Insights
    st.markdown("---")
    st.subheader("🤖 AI Benchmark Insights")
    with st.container(border=True):
        st.markdown(f"""
            **Quick Wins (0-30 days):**
            - Your **Days in A/R (57.9)** is currently below the 25th percentile (48.0). This is a critical area for improvement. 
            - Reducing this to the median (42.0) would improve cash velocity by estimated **$1.2M**.
            
            **Strategic Focus:**
            - **Clean Claim Rate (90.1%)** is close to the 50th percentile (92.0%). Targeting a 2% improvement here would reduce re-work costs significantly.
        """)
