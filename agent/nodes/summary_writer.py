import logging
from anthropic import Anthropic
from agent.state import AgentState
from config.settings import settings

logger = logging.getLogger(__name__)

SUMMARY_PROMPT = """
You are a Hospital Revenue Cycle Analyst.
You have been given a user's question and the data results from the analysis.
Your job is to provide a clear, professional, and data-backed answer.

CONTEXT:
User Question: {query}
Analysis Results: {results}

INSTRUCTIONS:
- Be concise but professional.
- Use the actual numbers provided in the results.
- If the result is missing or zero, note that data might be unavailable.
- Provide a brief insight if possible (e.g., "This is higher than usual" if obvious).
- Format your response in Markdown.
"""

def summary_writer_node(state: AgentState) -> AgentState:
    """Generates a natural language response using Claude."""
    
    user_query = state.get("user_query")
    data_result = state.get("data_result")
    
    if data_result is None:
        return {**state, "answer": "I found no data to answer that question."}

    try:
        client = Anthropic(api_key=settings.anthropic_api_key or "MOCK_KEY")
        
        if not settings.anthropic_api_key or settings.anthropic_api_key == "MOCK_KEY":
            # Mock summary generation
            metric_str = ", ".join([f"{k}: {v}" for k, v in data_result.items()])
            answer = f"Based on the analysis, the requested metrics are: **{metric_str}**. \n\n*This is a mock response because no API key was provided.*"
        else:
            prompt = SUMMARY_PROMPT.format(query=user_query, results=data_result)
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.content[0].text

        return {
            **state,
            "answer": answer
        }

    except Exception as e:
        logger.error(f"Error in summary_writer_node: {str(e)}")
        return {**state, "error": f"Failed to write summary: {str(e)}"}
