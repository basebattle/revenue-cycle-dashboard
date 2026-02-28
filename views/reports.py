import streamlit as st
import os
from datetime import datetime
from data.loader import DataLoader
from data.calculator import KPICalculator
from templates.board_deck import generate_board_deck

def render():
    st.header("📋 Report Generator")
    st.markdown("---")

    # 1. Template Selection
    st.subheader("Select Template")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Board Deck")
            st.write("Executive-level 10-slide deck with trends and recommendations.")
            if st.button("Select Board Deck"):
                st.session_state.selected_template = "board_deck"
                
    with col2:
        with st.container(border=True):
             st.markdown("### 📋 Monthly Ops")
             st.write("Operational KPI detail with drill-downs for department heads.")
             st.button("Select Monthly Ops", disabled=True)
             
    with col3:
        with st.container(border=True):
             st.markdown("### 💰 Payer Review")
             st.write("Payer-by-payer deep dive with denial analysis and benchmarks.")
             st.button("Select Payer Review", disabled=True)

    # 2. Configure
    if 'selected_template' in st.session_state:
        st.markdown("---")
        st.subheader(f"Configure: {st.session_state.selected_template.replace('_', ' ').title()}")
        
        with st.form("report_config"):
            col_a, col_b = st.columns(2)
            with col_a:
                start_date = st.date_input("Start Date", datetime(2025, 1, 1))
                payer = st.selectbox("Payer", ["All Payers", "UnitedHealthcare", "Aetna", "BCBS", "Medicare"])
            with col_b:
                end_date = st.date_input("End Date", datetime(2025, 12, 31))
                format_type = st.radio("Format", ["PPTX", "PDF (Coming Soon)"])
            
            submitted = st.form_submit_button("🚀 Generate Report")
            
            if submitted:
                 with st.spinner("Agent generating report..."):
                    loader = DataLoader()
                    calculator = KPICalculator()
                    df = loader.refresh_data()
                    kpis = calculator.calculate_all(df)
                    
                    filename = f"Board_Deck_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
                    # Correct export path inside the project
                    export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
                    os.makedirs(export_dir, exist_ok=True)
                    output_path = os.path.join(export_dir, filename)
                    
                    try:
                        generate_board_deck(kpis, output_path)
                        st.success(f"✅ Report generated successfully!")
                        
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="⬇️ Download PPTX Report",
                                data=file,
                                file_name=filename,
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )
                    except Exception as e:
                        st.error(f"Failed to generate report: {str(e)}")
