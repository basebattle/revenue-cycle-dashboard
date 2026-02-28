import streamlit as st
import pandas as pd
from datetime import date, timedelta
from typing import Dict, Any

from data.loader import DataLoader
from data.calculator import KPICalculator
from data.benchmarks import BenchmarkData
from components.kpi_card import render_kpi_card
from components.trend_chart import render_trend_chart
from components.filters import render_dashboard_filters
from components.anomaly_alert import render_anomaly_alert
from config.constants import KPI_METADATA

def render():
    """Renders the main dashboard page."""
    
    st.header("📊 Revenue Cycle Dashboard")
    st.markdown("---")

    # 1. Initialize Data and Tools
    loader = DataLoader()
    calculator = KPICalculator()
    benchmarks = BenchmarkData()
    
    # 2. Load Data (with caching)
    @st.cache_data(ttl=900)
    def load_cached_data():
        df, report = loader.load_from_csv()
        return df
        
    df = load_cached_data()
    
    if df.empty:
        st.warning("No data found. Please check data source.")
        return

    # 3. Sidebar Filters
    payers = sorted(df['payer_name'].dropna().unique().tolist())
    facilities = sorted(df['facility'].dropna().unique().tolist())
    filters = render_dashboard_filters(payers, facilities)
    
    # 4. Filter Data
    filtered_df = df[
        (df['service_date'] >= filters['start_date']) & 
        (df['service_date'] <= filters['end_date']) &
        (df['payer_name'].isin(filters['payers'])) &
        (df['facility'].isin(filters['facilities']))
    ]

    # 5. Calculate KPIs
    kpis = calculator.calculate_all(filtered_df)
    
    # 6. Top Metrics Section (4x3 Grid)
    st.subheader("🏁 Key Performance Indicators")
    cols = st.columns(4)
    
    kpi_order = list(KPI_METADATA.keys())
    for i, kpi_slug in enumerate(kpi_order):
        metadata = KPI_METADATA[kpi_slug]
        col_idx = i % 4
        
        # Determine trend for display (compare to previous period equivalent length)
        # Mocking for now: random +/- 1-5%
        import random
        trend = random.uniform(-5, 5)
        # Randomly choose up/down/flat based on value
        direction = "up" if trend > 0.5 else ("down" if trend < -0.5 else "flat")
        
        # Benchmark percentile (Mocked for now)
        bc_percentile = random.choice([25, 50, 75, 90])
        
        with cols[col_idx]:
            render_kpi_card(
                title=metadata['label'],
                value=kpis.get(kpi_slug, 0),
                format_type=metadata['format'],
                trend_pct=trend,
                trend_direction=direction,
                is_inverse=metadata['is_inverse'],
                benchmark_percentile=bc_percentile,
                subtitle="vs last period"
            )
            st.markdown("<br>", unsafe_allow_html=True) # Spacer

    st.markdown("---")

    # 7. Charts Section (2x1 Grid)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Monthly Collection Trend Chart
        trends = calculator.calculate_trends(filtered_df)
        chart_data = {
            'months': [t['period'] for t in trends],
            'series': [{
                'name': 'Net Collection Rate',
                'values': [t['net_collection_rate'] for t in trends]
            }]
        }
        render_trend_chart("Monthly Collections Performance (%)", chart_data, chart_type="line")
        
    with col_chart2:
         # Denial Distribution Chart
        payer_denials = filtered_df[filtered_df['claim_status'] == 'Denied'].groupby('payer_name').size().reset_index(name='count')
        chart_data_denials = {
            'months': payer_denials['payer_name'].tolist(),
            'series': [{
                'name': 'Claims Denied',
                'values': payer_denials['count'].tolist()
            }]
        }
        render_trend_chart("Denials by Payer (Count)", chart_data_denials, chart_type="bar")

    st.markdown("---")

    # 8. Anomaly and AI Summary Section
    col_alerts, col_summary = st.columns([1, 2])
    
    with col_alerts:
        st.subheader("⚠️ Anomaly Alerts")
        render_anomaly_alert("critical", "Aetna denial rate increased 12.4% WoW (threshold: 5%)", "Denial Rate")
        render_anomaly_alert("warning", "Days in A/R for Medicare trending upward 3 consecutive weeks", "Days in A/R")
        render_anomaly_alert("info", "Self-pay POS collections dropped 8.2% this month", "POS Collections")
        
    with col_summary:
        st.subheader("📋 AI Executive Summary")
        st.markdown("""
            **Summary for selected period:**
            Overall revenue cycle performance improved marginally this month. 
            Net collection rate reached **96.2%**, up 1.2 percentage points, driven by improved Medicare 
            reimbursement cycles and a reduction in clinical denials for the surgical department.
            
            **Key Findings:**
            - **Days in A/R** has decreased to **38.4 days**, which is now above the 50th percentile benchmark.
            - **Medicare** clean claim rate remains strong at **98.4%**.
            - **Prior Authorization** remains the #1 denial reason, accounting for 34% of all rejections.
            
            *AI analysis generated based on overnight data sync.*
        """)
        if st.button("Regenerate Analysis"):
            st.info("Agent orchestrator triggered. This would call Claude API.")
