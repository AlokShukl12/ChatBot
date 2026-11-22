
import streamlit as st
import uuid
import html

from backend import workflow
from langchain_core.messages import HumanMessage

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.user-message {
    display: flex;
    justify-content: flex-start;
    margin: 15px 0;
}

.ai-message {
    display: flex;
    justify-content: flex-end;
    margin: 15px 0;
}

.message {
    padding: 12px 18px;
    border-radius: 15px;
    max-width: 75%;
    overflow-wrap: anywhere;
    color: white;
    font-size: 16px;
}

.user-message .message {
    background-color: #343541;
    border-bottom-left-radius: 3px;
}

.ai-message .message {
    background-color: #2563eb;
    border-bottom-right-radius: 3px;
}

.chat-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    '<div class="chat-title">🤖 Welcome to AI Chatbot</div>',
    unsafe_allow_html=True
)

st.caption("Your personal AI assistant. Ask me anything!")

# Initialize session state
if "message_history" not in st.session_state:
    st.session_state.message_history = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# LangGraph configuration
CONFIG = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.message_history = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")
    st.write("💬 Total Messages:",
             len(st.session_state.message_history))

    st.caption("Powered by LangGraph + Streamlit")

# Display chat history
for message in st.session_state.message_history:

    safe_content = html.escape(message["content"]).replace("\n", "<br>")

    if message["role"] == "user":
        st.markdown(
            f"""
            <div class="user-message">
                <div class="message">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="ai-message">
                <div class="message">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Chat input
user_input = st.chat_input("💬 Type your message here...")

if user_input:

    # Save user message
    st.session_state.message_history.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    safe_input = html.escape(user_input).replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="user-message">
            <div class="message">{safe_input}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate AI response
    with st.spinner("🤖 AI is thinking..."):

        try:
            response = workflow.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=CONFIG
            )

            ai_message = response["messages"][-1].content

            # Save AI response
            st.session_state.message_history.append({
                "role": "assistant",
                "content": ai_message
            })

            # Display AI response
            safe_response = html.escape(str(ai_message)).replace("\n", "<br>")

            st.markdown(
                f"""
                <div class="ai-message">
                    <div class="message">{safe_response}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Error: {e}")
