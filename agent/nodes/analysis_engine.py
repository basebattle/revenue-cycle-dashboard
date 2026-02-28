import pandas as pd
import logging
from typing import Dict, Any
from agent.state import AgentState
from data.loader import DataLoader
from data.calculator import KPICalculator

logger = logging.getLogger(__name__)

def analysis_engine_node(state: AgentState) -> AgentState:
    """Executes data analysis and KPI calculations based on intent."""
    
    intent = state.get("intent")
    metrics = state.get("metrics", [])
    filters = state.get("filters", {})
    
    if not intent or not metrics:
        return {**state, "error": "Missing intent or metrics for analysis"}

    try:
        loader = DataLoader()
        calculator = KPICalculator()
        
        # 1. Load Data
        df = loader.refresh_data()
        if df.empty:
            return {**state, "error": "No data available for analysis"}

        # 2. Apply Filters from Intent
        filtered_df = df.copy()
        if filters:
            if filters.get("payer"):
                filtered_df = filtered_df[filtered_df['payer_name'] == filters["payer"]]
            
            # Simple date range parsing for demo (e.g. "Q4")
            # In real system, this would be more robust
            if filters.get("date_range") == "Q4":
                filtered_df = filtered_df[pd.to_datetime(filtered_df['service_date']).dt.quarter == 4]
            elif filters.get("date_range") == "2025":
                filtered_df = filtered_df[pd.to_datetime(filtered_df['service_date']).dt.year == 2025]

        # 3. Calculate Results
        if intent == "comparison":
            # Comparison logic: compare filtered vs full or specified periods
            # For now, just calculate the metrics for the filtered set
            result = calculator.calculate_all(filtered_df)
        else:
            # Standard KPI query
            result = calculator.calculate_all(filtered_df)

        # 4. Filter result to only requested metrics
        final_result = {m: result.get(m) for m in metrics if m in result}

        return {
            **state,
            "data_result": final_result
        }

    except Exception as e:
        logger.error(f"Error in analysis_engine_node: {str(e)}")
        return {**state, "error": f"Analysis failed: {str(e)}"}
