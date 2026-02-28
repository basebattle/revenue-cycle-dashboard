from typing import Literal
from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes.query_parser import query_parser_node
from .nodes.analysis_engine import analysis_engine_node
from .nodes.summary_writer import summary_writer_node

def orchestrator():
    """Builds and returns the LangGraph state machine."""
    
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("parser", query_parser_node)
    workflow.add_node("analyzer", analysis_engine_node)
    workflow.add_node("writer", summary_writer_node)

    # 2. Define Edges
    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "analyzer")
    workflow.add_edge("analyzer", "writer")
    workflow.add_edge("writer", END)

    # 3. Compile
    return workflow.compile()

# Singleton instance
agent_app = orchestrator()

def run_agent(query: str, session_id: str = "default") -> dict:
    """Entry point to run the agent on a specific query."""
    inputs = {
        "user_query": query,
        "session_id": session_id,
        "iteration_count": 0
    }
    
    # Run the graph
    final_state = agent_app.invoke(inputs)
    return final_state
