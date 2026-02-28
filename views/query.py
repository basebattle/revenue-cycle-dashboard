import streamlit as st
from agent.orchestrator import run_agent
from components.chat_message import render_chat_message

def render():
    """Renders the AI Query Console page."""
    
    st.header("💬 AI Query Console")
    st.markdown("---")

    # 1. Initialize Session State for Chat
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "agent", "content": "Hello! I'm your Revenue Cycle AI Agent. Ask me anything about collections, denials, or A/R trends."}
        ]

    # 2. Display Message History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            render_chat_message(msg["role"], msg["content"])

    # 3. Chat Input
    if prompt := st.chat_input("Ask about your revenue cycle..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            render_chat_message("user", prompt)

        # 4. Run Agent
        with st.spinner("🤖 Thinking..."):
            try:
                result = run_agent(prompt)
                answer = result.get("answer", "I'm sorry, I couldn't process that query.")
                
                # Add agent message
                st.session_state.messages.append({"role": "agent", "content": answer})
                with chat_container:
                    render_chat_message("agent", answer)
            except Exception as e:
                st.error(f"Agent error: {str(e)}")

    # 5. Sidebar Options
    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Try These Queries")
    sample_queries = [
        "What's our denial rate for Aetna in Q4?",
        "Show me collections performance for 2025",
        "Which payer has the highest denial rate?",
        "Compare collections in Q3 vs Q4"
    ]
    
    for q in sample_queries:
        if st.sidebar.button(q):
            # This would trigger the chat with this query
            # For simplicity in this demo, it just fills the prompt
            st.info(f"Copy/paste this query: {q}")
            
    if st.sidebar.button("🗑️ Clear History"):
        st.session_state.messages = [
            {"role": "agent", "content": "History cleared. How can I help you today?"}
        ]
        st.rerun()
