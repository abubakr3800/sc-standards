"""
Web Interface for Lighting Standards Chat
Simple Streamlit interface for the chat API
"""
import streamlit as st
import requests
import json
from typing import Dict, List

# Configure Streamlit page
st.set_page_config(
    page_title="Lighting Standards Chat",
    page_icon="💡",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

def send_message(message: str) -> Dict:
    """Send message to the chat API"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": message}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "answer": "Sorry, I couldn't process your request. Please try again.",
                "confidence": 0.0,
                "sources": [],
                "recommendations": []
            }
    except requests.exceptions.ConnectionError:
        return {
            "answer": "Cannot connect to the API. Please make sure the API server is running on port 8000.",
            "confidence": 0.0,
            "sources": [],
            "recommendations": []
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "confidence": 0.0,
            "sources": [],
            "recommendations": []
        }

def main():
    """Main Streamlit app"""
    st.title("💡 Lighting Standards Chat")
    st.markdown("Ask questions about lighting standards and get instant answers!")
    
    # Sidebar with help
    with st.sidebar:
        st.header("📚 Help")
        st.markdown("""
        **Example Questions:**
        - What is the illuminance requirement for office work?
        - What is the UGR limit for conference rooms?
        - What is the recommended CRI for office lighting?
        - What is the power density limit for office lighting?
        - What is illuminance?
        - What is UGR?
        - What is CRI?
        """)
        
        st.markdown("""
        **Supported Applications:**
        - Office
        - Conference
        - Corridor
        - Reception
        - Staircase
        - Detailed work
        """)
        
        st.markdown("""
        **Supported Parameters:**
        - Illuminance
        - UGR
        - CRI
        - Power density
        - Uniformity
        """)
        
        # API status
        st.header("🔗 API Status")
        try:
            response = requests.get(f"{API_URL}/")
            if response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ API Offline")
            st.markdown("Start the API with: `python chat_api.py`")
    
    # Main chat interface
    st.header("💬 Chat with Lighting Standards")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show additional info for assistant messages
            if message["role"] == "assistant" and "confidence" in message:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Confidence", f"{message['confidence']:.1%}")
                with col2:
                    st.metric("Sources", len(message.get("sources", [])))
                
                if message.get("sources"):
                    with st.expander("📖 Sources"):
                        for source in message["sources"]:
                            st.write(f"• {source}")
                
                if message.get("recommendations"):
                    with st.expander("💡 Recommendations"):
                        for rec in message["recommendations"]:
                            st.write(f"• {rec}")
    
    # Chat input
    if prompt := st.chat_input("Ask about lighting standards..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(prompt)
            
            # Display response
            st.markdown(response["answer"])
            
            # Show confidence and sources
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Confidence", f"{response['confidence']:.1%}")
            with col2:
                st.metric("Sources", len(response.get("sources", [])))
            
            # Show sources
            if response.get("sources"):
                with st.expander("📖 Sources"):
                    for source in response["sources"]:
                        st.write(f"• {source}")
            
            # Show recommendations
            if response.get("recommendations"):
                with st.expander("💡 Recommendations"):
                    for rec in response["recommendations"]:
                        st.write(f"• {rec}")
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["answer"],
            "confidence": response["confidence"],
            "sources": response.get("sources", []),
            "recommendations": response.get("recommendations", [])
        })
    
    # Quick question buttons
    st.header("🚀 Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Office Illuminance"):
            st.session_state.messages.append({"role": "user", "content": "What is the illuminance requirement for office work?"})
            st.rerun()
        
        if st.button("Conference UGR"):
            st.session_state.messages.append({"role": "user", "content": "What is the UGR limit for conference rooms?"})
            st.rerun()
    
    with col2:
        if st.button("Office CRI"):
            st.session_state.messages.append({"role": "user", "content": "What is the recommended CRI for office lighting?"})
            st.rerun()
        
        if st.button("Power Density"):
            st.session_state.messages.append({"role": "user", "content": "What is the power density limit for office lighting?"})
            st.rerun()
    
    with col3:
        if st.button("What is Illuminance?"):
            st.session_state.messages.append({"role": "user", "content": "What is illuminance?"})
            st.rerun()
        
        if st.button("What is UGR?"):
            st.session_state.messages.append({"role": "user", "content": "What is UGR?"})
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
