from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    """Represents the state of the revenue cycle analytics agent."""
    
    # Input
    user_query: str
    session_id: str
    
    # Parsed Intent
    intent: Optional[str] # "kpi_query", "comparison", "forecast", "anomaly", "report"
    metrics: Optional[List[str]] # ["denial_rate", "net_collection_rate"]
    filters: Optional[Dict[str, Any]] # {"payer": "Aetna", "date_range": {...}}
    comparison_type: Optional[str] # "period_over_period", "payer_vs_payer", "benchmark"
    
    # Computed Data
    data_result: Optional[Dict[str, Any]] # Raw calculation output
    chart_config: Optional[Dict[str, Any]] # Plotly chart specification
    anomalies: Optional[List[Dict[str, Any]]] # Detected anomalies
    
    # Output
    answer: Optional[str] # Natural language response
    summary: Optional[str] # Executive summary text
    report_path: Optional[str] # Path to generated file
    error: Optional[str] # Error message if pipeline fails
    
    # Control
    next_node: Optional[str] # Router decision
    iteration_count: int # Prevent infinite loops
