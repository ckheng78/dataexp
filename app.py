import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os
import time
from datetime import datetime

# Add the src directory to the path so we can import dataexp
sys.path.append(str(Path(__file__).parent / "src"))

from dataexp.crew import Dataexp
from dataexp.tools.data_tool import (
    get_column_names, 
    get_dataframe_info, 
    execute_sql_on_csv,
    save_dataframe,
    load_dataframe
)

# Page configuration
st.set_page_config(
    page_title="DataExp - AI Data Explorer Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chatbot interface
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    
    .chat-container {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 70%;
        margin-left: auto;
        margin-right: 0;
        word-wrap: break-word;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 70%;
        margin-left: 0;
        margin-right: auto;
        word-wrap: break-word;
    }
    
    .agent-header {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6B7280;
        margin-bottom: 0.5rem;
    }
    
    .timestamp {
        font-size: 0.75rem;
        color: #9CA3AF;
        margin-top: 0.25rem;
    }
    
    .thinking-indicator {
        background-color: #FEF3C7;
        color: #92400E;
        border-radius: 12px;
        padding: 8px 12px;
        margin: 8px 0;
        font-style: italic;
        border: 1px solid #FCD34D;
    }
    
    .sidebar-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
    }
    
    .quick-question {
        background-color: #EFF6FF;
        border: 1px solid #DBEAFE;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px 0;
        cursor: pointer;
        font-size: 0.9rem;
        color: #1E40AF;
        transition: all 0.3s ease;
    }
    
    .quick-question:hover {
        background-color: #DBEAFE;
        transform: translateY(-1px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #E5E7EB;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Dark mode compatibility */
    @media (prefers-color-scheme: dark) {
        .chat-container {
            background-color: #1F2937;
            border: 1px solid #374151;
            color: #F9FAFB;
        }
        
        .user-message {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        }
        
        .ai-message {
            background: linear-gradient(135deg, #EC4899 0%, #EF4444 100%);
        }
        
        .thinking-indicator {
            background-color: #451A03;
            color: #FCD34D;
            border: 1px solid #92400E;
        }
        
        .quick-question {
            background-color: #1E3A8A;
            border: 1px solid #3B82F6;
            color: #DBEAFE;
        }
        
        .quick-question:hover {
            background-color: #1E40AF;
        }
        
        .agent-header {
            color: #D1D5DB;
        }
        
        .timestamp {
            color: #6B7280;
        }
        
        .sidebar-header {
            color: #F9FAFB;
        }
        
        .stTextInput > div > div > input {
            background-color: #1F2937 !important;
            color: #F9FAFB !important;
            border: 2px solid #374151 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'crew' not in st.session_state:
        st.session_state.crew = None
    if 'data_file' not in st.session_state:
        st.session_state.data_file = str(Path("src/dataexp/data/titanic.csv"))

def get_crew():
    """Get or create CrewAI crew instance"""
    if st.session_state.crew is None:
        try:
            st.session_state.crew = Dataexp()
        except Exception as e:
            st.error(f"Error initializing CrewAI: {str(e)}")
            return None
    return st.session_state.crew

def add_message(role, content, timestamp=None, agent=None):
    """Add a message to the chat history"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    
    message = {
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "agent": agent
    }
    st.session_state.messages.append(message)

def display_chat_history():
    """Display the chat history"""
    st.markdown("## 💬 Chat History")
    
    if not st.session_state.messages:
        st.markdown("""
        <div class="chat-container">
            <div class="ai-message">
                <div class="agent-header">🤖 AI Assistant</div>
                Hello! I'm your AI data exploration assistant. I can help you analyze the Titanic dataset. 
                Feel free to ask me questions like:
                <ul>
                    <li>What's the survival rate by gender?</li>
                    <li>How many passengers were in each class?</li>
                    <li>What was the average age of survivors?</li>
                    <li>Show me a visualization of passenger ages</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display messages in reverse order (newest first)
    for message in reversed(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-container">
                <div class="user-message">
                    <div class="agent-header">👤 You</div>
                    {message["content"]}
                    <div class="timestamp">{message["timestamp"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            agent_emoji = "🤖" if not message.get("agent") else "🔍"
            agent_name = message.get("agent", "AI Assistant")
            
            st.markdown(f"""
            <div class="chat-container">
                <div class="ai-message">
                    <div class="agent-header">{agent_emoji} {agent_name}</div>
                    {message["content"]}
                    <div class="timestamp">{message["timestamp"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def process_user_question(question):
    """Process user question with CrewAI agents"""
    crew = get_crew()
    if crew is None:
        return "Sorry, I'm having trouble connecting to the AI agents. Please try again."
    
    try:
        # Show thinking indicator
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("""
        <div class="thinking-indicator">
            🤔 AI agents are thinking... This may take a moment.
        </div>
        """, unsafe_allow_html=True)
        
        # Create progress bar
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        # Run the crew with the user's question
        inputs = {
            'user_input': question,
            'data_file': st.session_state.data_file
        }
        
        result = crew.crew().kickoff(inputs=inputs)
        
        # Clear thinking indicator and progress bar
        thinking_placeholder.empty()
        progress_bar.empty()
        
        # Process the result
        if hasattr(result, 'raw'):
            response = result.raw
        else:
            response = str(result)
        
        return response
        
    except Exception as e:
        thinking_placeholder.empty()
        if 'progress_bar' in locals():
            progress_bar.empty()
        return f"I encountered an error while processing your question: {str(e)}"

def display_quick_questions():
    """Display quick question buttons in sidebar"""
    st.markdown('<div class="sidebar-header">💡 Quick Questions</div>', unsafe_allow_html=True)
    
    quick_questions = [
        "What's the overall survival rate?",
        "How many passengers were in each class?",
        "What was the average age of passengers?",
        "Show me survival rate by gender",
        "How many children were on board?",
        "What's the survival rate by passenger class?",
        "Show me the age distribution",
        "Which deck had the most passengers?",
        "What was the fare range?",
        "Show me passenger embarkation ports"
    ]
    
    for question in quick_questions:
        if st.button(question, key=f"quick_{question}", help="Click to ask this question"):
            return question
    
    return None

def create_visualization_from_data(data, question):
    """Create visualizations based on data and question context"""
    try:
        if not data or len(data) == 0:
            return None
            
        df = pd.DataFrame(data)
        
        # Determine chart type based on question keywords and data
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['survival', 'survived', 'death', 'died']):
            if 'gender' in question_lower or 'sex' in question_lower:
                # Survival by gender
                fig = px.bar(df, x='Sex', y='count', color='Survived', 
                           title='Survival by Gender', 
                           color_discrete_map={'Survived': '#10B981', 'Did not survive': '#EF4444'})
            elif 'class' in question_lower:
                # Survival by class
                fig = px.bar(df, x='Pclass', y='count', color='Survived',
                           title='Survival by Passenger Class',
                           color_discrete_map={'Survived': '#10B981', 'Did not survive': '#EF4444'})
            else:
                # General survival
                fig = px.pie(df, values='count', names='Survived', 
                           title='Overall Survival Rate',
                           color_discrete_map={'Survived': '#10B981', 'Did not survive': '#EF4444'})
        
        elif 'age' in question_lower and 'distribution' in question_lower:
            # Age distribution histogram
            fig = px.histogram(df, x='Age', nbins=30, title='Age Distribution of Passengers')
            
        elif 'age' in question_lower:
            # Age-related bar chart
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                        title='Age Analysis')
        
        elif 'class' in question_lower:
            # Passenger class distribution
            fig = px.bar(df, x='Pclass', y='count', 
                        title='Passengers by Class',
                        color='Pclass')
        
        elif 'fare' in question_lower:
            # Fare analysis
            if 'range' in question_lower:
                fig = px.histogram(df, x='Fare', nbins=20, title='Fare Distribution')
            else:
                fig = px.box(df, y='Fare', title='Fare Analysis')
        
        elif 'embark' in question_lower or 'port' in question_lower:
            # Embarkation ports
            fig = px.bar(df, x='Embarked', y='count', 
                        title='Passengers by Embarkation Port',
                        color='Embarked')
        
        else:
            # Default: create appropriate chart based on data structure
            if len(df.columns) == 2:
                if df[df.columns[1]].dtype in ['int64', 'float64']:
                    # Numeric data - bar chart
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1])
                else:
                    # Categorical data - pie chart
                    fig = px.pie(df, values=df.columns[1], names=df.columns[0])
            else:
                # Multi-column data - use first two columns
                fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
        
        # Customize chart appearance
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151'),
            title_font_size=16
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        return None

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #374151; font-size: 2.5rem; font-weight: 300; margin-bottom: 0.5rem;">
            🤖 AI Data Explorer
        </h1>
        <p style="color: #6B7280; font-size: 1.1rem; font-weight: 300;">
            Chat with AI agents to explore the Titanic dataset
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if dataset exists
    if not Path(st.session_state.data_file).exists():
        st.error(f"❌ Titanic dataset not found at: {st.session_state.data_file}")
        st.info("Please ensure the titanic.csv file is located in src/dataexp/data/")
        return
    
    # Sidebar with quick questions and dataset info
    with st.sidebar:
        st.markdown("## 🚢 Titanic Dataset Explorer")
        
        # Dataset info
        st.markdown("### 📊 Dataset Information")
        try:
            df = pd.read_csv(st.session_state.data_file)
            st.metric("Total Passengers", len(df))
            st.metric("Survivors", len(df[df['Survived'] == 1]))
            st.metric("Survival Rate", f"{len(df[df['Survived'] == 1])/len(df)*100:.1f}%")
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")
        
        st.markdown("---")
        
        # Quick questions
        selected_question = display_quick_questions()
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", help="Clear all chat history"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat history
        display_chat_history()
        
        # Chat input
        st.markdown("## 💭 Ask a Question")
        
        # Handle quick question selection
        if selected_question:
            user_input = selected_question
        else:
            user_input = st.text_input(
                "Type your question about the Titanic dataset:",
                placeholder="e.g., What's the survival rate by gender?",
                key="user_input"
            )
        
        # Process question
        if st.button("🚀 Send", key="send_button") and user_input:
            # Add user message
            add_message("user", user_input)
            
            # Process with AI agents
            response = process_user_question(user_input)
            
            # Add AI response
            add_message("assistant", response, agent="Data Analysis Team")
            
            # Try to extract and visualize data if the response contains structured data
            try:
                # Look for JSON data in the response
                if "{" in response and "}" in response:
                    # Try to extract JSON data for visualization
                    import re
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group()
                        try:
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 0:
                                fig = create_visualization_from_data(data, user_input)
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True)
                        except:
                            pass
            except:
                pass
            
            # Rerun to update the interface
            st.rerun()
    
    with col2:
        # Data preview
        st.markdown("### 📋 Data Preview")
        try:
            df = pd.read_csv(st.session_state.data_file)
            st.dataframe(df.head(), use_container_width=True, height=300)
        except Exception as e:
            st.error(f"Error loading data preview: {str(e)}")

if __name__ == "__main__":
    main()
