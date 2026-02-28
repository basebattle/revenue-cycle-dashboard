import json
import logging
from typing import Dict, Any
from anthropic import Anthropic
from agent.state import AgentState
from config.settings import settings

logger = logging.getLogger(__name__)

# Prompt for the query parser
QUERY_PARSER_PROMPT = """
You are a specialized query parser for a Hospital Revenue Cycle Dashboard.
Your job is to convert a user's natural language question into a structured JSON object.

CORE KPIs:
- net_collection_rate
- gross_collection_rate
- days_in_ar
- clean_claim_rate
- denial_rate
- denial_overturn_rate
- cost_to_collect
- charge_lag
- ar_over_90_pct
- cash_as_pct_nr
- bad_debt_rate
- pos_collection_rate

PAYERS:
- UnitedHealthcare, Aetna, BCBS, Medicare, Medicaid, Self-Pay

OUTPUT FORMAT:
{
    "intent": "kpi_query" | "comparison" | "anomaly" | "report",
    "metrics": ["metric1", "metric2"],
    "filters": {
        "payer": "PayerName" | null,
        "date_range": "Q1" | "Q2" | "Q3" | "Q4" | "2024" | "2025" | null,
        "facility": "FacilityName" | null
    },
    "comparison_type": "period_over_period" | "payer_vs_payer" | "benchmark" | null
}

EXAMPLES:
1. "What's our denial rate for Aetna in Q4?"
   {"intent": "kpi_query", "metrics": ["denial_rate"], "filters": {"payer": "Aetna", "date_range": "Q4"}, "comparison_type": null}

2. "Compare Medicare collections in Q3 vs Q4"
   {"intent": "comparison", "metrics": ["net_collection_rate"], "filters": {"payer": "Medicare"}, "comparison_type": "period_over_period"}

3. "Show me anomalies in our collections this month"
   {"intent": "anomaly", "metrics": ["net_collection_rate"], "filters": null, "comparison_type": null}

Respond with VALID JSON only.
"""

def query_parser_node(state: AgentState) -> AgentState:
    """Parses user query into structured intent using Claude."""
    
    user_query = state.get("user_query", "")
    if not user_query:
        return {**state, "error": "Empty user query"}

    try:
        # Initialize Anthropic client
        # In a real app, this key would be in settings.anthropic_api_key
        # For this environment, we use the available LLM capabilities
        client = Anthropic(api_key=settings.anthropic_api_key or "MOCK_KEY")
        
        # If no real API key, we mock the response for demonstration
        if not settings.anthropic_api_key or settings.anthropic_api_key == "MOCK_KEY":
             logger.warning("No Anthropic API key found. Using mock parser.")
             # Simple heuristic parser for demo
             if "denial" in user_query.lower():
                 parsed = {"intent": "kpi_query", "metrics": ["denial_rate"], "filters": {"payer": "Aetna" if "aetna" in user_query.lower() else None}, "comparison_type": None}
             elif "compare" in user_query.lower():
                 parsed = {"intent": "comparison", "metrics": ["net_collection_rate"], "filters": {}, "comparison_type": "period_over_period"}
             else:
                 parsed = {"intent": "kpi_query", "metrics": ["net_collection_rate"], "filters": {}, "comparison_type": None}
        else:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                temperature=0,
                system=QUERY_PARSER_PROMPT,
                messages=[{"role": "user", "content": user_query}]
            )
            parsed = json.loads(response.content[0].text)

        return {
            **state,
            "intent": parsed.get("intent"),
            "metrics": parsed.get("metrics"),
            "filters": parsed.get("filters"),
            "comparison_type": parsed.get("comparison_type")
        }

    except Exception as e:
        logger.error(f"Error in query_parser_node: {str(e)}")
        return {**state, "error": f"Failed to parse query: {str(e)}"}
