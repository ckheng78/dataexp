import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

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
    page_title="DataExp - Titanic Data Explorer",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean light theme with dark mode compatibility
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .main-header {
        font-size: 1rem;
        font-weight: 200;
        color: #2E4057;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    .analysis-container {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .result-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #D1D5DB;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    .stButton > button {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2563EB;
        transform: translateY(-1px);
    }
    .metric-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #E5E7EB;
        margin: 0.5rem;
    }
    
    /* Dark mode compatibility fixes */
    .stSelectbox > div > div > div {
        background-color: var(--background-color, #FFFFFF) !important;
        color: var(--text-color, #000000) !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: var(--text-color, #000000) !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: var(--background-color, #FFFFFF) !important;
        color: var(--text-color, #000000) !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        font-family: 'Monaco', 'Menlo', 'Consolas', monospace !important;
    }
    
    .stTextInput > div > div > input {
        background-color: var(--background-color, #FFFFFF) !important;
        color: var(--text-color, #000000) !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
    }
    
    /* Dark mode specific overrides */
    @media (prefers-color-scheme: dark) {
        .stSelectbox > div > div > div {
            background-color: #1F2937 !important;
            color: #F9FAFB !important;
            border: 1px solid #374151 !important;
        }
        
        .stSelectbox > div > div > div > div {
            color: #F9FAFB !important;
        }
        
        .stTextArea > div > div > textarea {
            background-color: #1F2937 !important;
            color: #F9FAFB !important;
            border: 1px solid #374151 !important;
        }
        
        .stTextInput > div > div > input {
            background-color: #1F2937 !important;
            color: #F9FAFB !important;
            border: 1px solid #374151 !important;
        }
        
        .analysis-container {
            background-color: #111827 !important;
            border: 1px solid #374151 !important;
            color: #F9FAFB !important;
        }
        
        .result-container {
            background-color: #1F2937 !important;
            border: 1px solid #374151 !important;
            color: #F9FAFB !important;
        }
        
        .main-header {
            color: #F9FAFB !important;
        }
        
        .sub-header {
            color: #D1D5DB !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚢 Titanic Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore the Titanic dataset with AI-powered analysis</p>', unsafe_allow_html=True)
    
    # Dataset path (fixed to Titanic)
    data_file = str(Path("src/dataexp/data/titanic.csv"))
    
    # Check if dataset exists
    if not Path(data_file).exists():
        st.error(f"❌ Titanic dataset not found at: {data_file}")
        st.info("Please ensure the titanic.csv file is located in src/dataexp/data/")
        return
    
    # Dataset Overview Section
    st.markdown("## 📊 Dataset Overview")
    
    # Quick stats in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Show Dataset Info", help="View dataset structure and sample data"):
            show_dataset_info(data_file)
    
    with col2:
        if st.button("🔍 Quick Stats", help="View basic statistics"):
            show_quick_stats(data_file)
    
    with col3:
        if st.button("📈 Data Summary", help="View data distribution"):
            show_data_summary(data_file)
    
    with col4:
        if st.button("🧹 Data Quality", help="Check for missing values"):
            show_data_quality(data_file)
    
    st.markdown("---")
    
    # Analysis Section
    st.markdown("## 🤖 Data Analysis")
    
    # Analysis mode selection
    analysis_mode = st.radio(
        "Choose your analysis method:",
        ["🧠 AI-Powered Analysis", "💻 Direct SQL Query"],
        horizontal=True,
        help="AI analysis uses CrewAI agents to understand your questions"
    )
    
    if analysis_mode == "🧠 AI-Powered Analysis":
        ai_analysis_section(data_file)
    else:
        sql_analysis_section(data_file)

def show_dataset_info(data_file):
    """Display dataset information in a clean format"""
    with st.spinner("Loading dataset information..."):
        try:
            info_result = get_dataframe_info.run(data_file)
            info_data = json.loads(info_result)
            
            if "error" in info_data:
                st.error(f"Error: {info_data['error']}")
                return
            
            # Display in clean containers
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            
            # Basic metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Rows", f"{info_data['shape'][0]:,}")
            with col2:
                st.metric("📋 Columns", info_data['shape'][1])
            with col3:
                missing_count = sum(info_data['null_counts'].values())
                st.metric("❌ Missing Values", f"{missing_count:,}")
            
            # Column information
            st.markdown("### Column Information")
            columns_df = pd.DataFrame(info_data["columns"])
            st.dataframe(columns_df, use_container_width=True, hide_index=True)
            
            # Sample data
            st.markdown("### Sample Data")
            sample_df = pd.DataFrame(info_data["sample_data"])
            st.dataframe(sample_df, use_container_width=True, hide_index=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")

def show_quick_stats(data_file):
    """Show quick statistics"""
    with st.spinner("Generating quick statistics..."):
        try:
            # Get basic stats using SQL
            queries = [
                ("Total Passengers", "SELECT COUNT(*) as count FROM df"),
                ("Survivors", "SELECT COUNT(*) as count FROM df WHERE Survived = 1"),
                ("Average Age", "SELECT ROUND(AVG(Age), 1) as avg_age FROM df WHERE Age IS NOT NULL"),
                ("Classes", "SELECT COUNT(DISTINCT Pclass) as classes FROM df")
            ]
            
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            cols = st.columns(len(queries))
            
            for i, (label, query) in enumerate(queries):
                result = execute_sql_on_csv.run(data_file, query)
                data = json.loads(result)
                if "error" not in data and len(data) > 0:
                    value = list(data[0].values())[0]
                    with cols[i]:
                        st.metric(label, value)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error generating stats: {str(e)}")

def show_data_summary(data_file):
    """Show data distribution summary"""
    with st.spinner("Analyzing data distribution..."):
        try:
            # Get survival distribution
            survival_query = "SELECT Survived, COUNT(*) as count FROM df GROUP BY Survived"
            result = execute_sql_on_csv.run(data_file, survival_query)
            data = json.loads(result)
            
            if "error" not in data:
                df = pd.DataFrame(data)
                df['Survived'] = df['Survived'].map({0: 'Did not survive', 1: 'Survived'})
                
                st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Survival Distribution")
                    fig = px.pie(df, values='count', names='Survived', 
                               color_discrete_map={'Survived': '#10B981', 'Did not survive': '#EF4444'})
                    fig.update_layout(showlegend=True, height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### Passenger Classes")
                    class_query = "SELECT Pclass, COUNT(*) as count FROM df GROUP BY Pclass ORDER BY Pclass"
                    class_result = execute_sql_on_csv(data_file, class_query)
                    class_data = json.loads(class_result)
                    
                    if "error" not in class_data:
                        class_df = pd.DataFrame(class_data)
                        class_df['Pclass'] = 'Class ' + class_df['Pclass'].astype(str)
                        fig = px.bar(class_df, x='Pclass', y='count', color='Pclass')
                        fig.update_layout(showlegend=False, height=300)
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error analyzing data: {str(e)}")

def show_data_quality(data_file):
    """Show data quality information"""
    with st.spinner("Checking data quality..."):
        try:
            info_result = get_dataframe_info.run(data_file)
            info_data = json.loads(info_result)
            
            if "error" in info_data:
                st.error(f"Error: {info_data['error']}")
                return
            
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            
            null_counts = info_data["null_counts"]
            if any(count > 0 for count in null_counts.values()):
                st.markdown("### Missing Values by Column")
                null_df = pd.DataFrame(list(null_counts.items()), columns=["Column", "Missing Count"])
                null_df = null_df[null_df["Missing Count"] > 0]
                null_df["Percentage"] = (null_df["Missing Count"] / info_data["shape"][0] * 100).round(2)
                
                fig = px.bar(null_df, x="Column", y="Missing Count", 
                           title="Missing Values by Column")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(null_df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ No missing values found in the dataset!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error checking data quality: {str(e)}")

def ai_analysis_section(data_file):
    """AI-powered analysis section"""
    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
    
    # Predefined questions for quick access
    st.markdown("### 💡 Quick Questions")
    quick_questions = [
        "What is the survival rate by passenger class?",
        "What is the average age of passengers by gender?",
        "How does the fare relate to survival?",
        "What is the family size distribution?",
        "Which port of embarkation had the highest survival rate?"
    ]
    
    selected_question = st.selectbox("Choose a predefined question:", 
                                   ["Custom question..."] + quick_questions)
    
    if selected_question != "Custom question...":
        user_query = selected_question
    else:
        user_query = st.text_area(
            "Or ask your own question:",
            placeholder="e.g., What factors influenced survival the most?",
            height=100
        )
    
    if st.button("🚀 Analyze with AI", type="primary"):
        if not user_query or not user_query.strip():
            st.warning("Please enter a question or select a predefined one.")
            return
        
        analyze_with_ai(data_file, user_query)
    
    st.markdown('</div>', unsafe_allow_html=True)

def sql_analysis_section(data_file):
    """Direct SQL analysis section"""
    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
    
    # SQL examples
    st.markdown("### 📝 SQL Examples")
    examples = {
        "Basic Selection": "SELECT * FROM df LIMIT 10",
        "Survival by Class": "SELECT Pclass, AVG(Survived) as survival_rate FROM df GROUP BY Pclass",
        "Age Statistics": "SELECT Sex, AVG(Age) as avg_age, COUNT(*) as count FROM df WHERE Age IS NOT NULL GROUP BY Sex",
        "Fare Analysis": "SELECT Pclass, AVG(Fare) as avg_fare, MAX(Fare) as max_fare FROM df GROUP BY Pclass"
    }
    
    selected_example = st.selectbox("Choose an example query:", 
                                  ["Custom query..."] + list(examples.keys()))
    
    if selected_example != "Custom query...":
        default_query = examples[selected_example]
    else:
        default_query = ""
    
    sql_query = st.text_area(
        "Enter your SQL query (use 'df' as table name):",
        value=default_query,
        height=120,
        help="Remember to use 'df' as the table name in your queries"
    )
    
    if st.button("▶️ Execute Query", type="primary"):
        if not sql_query or not sql_query.strip():
            st.warning("Please enter a SQL query.")
            return
        
        execute_sql_query.run(data_file, sql_query)
    
    st.markdown('</div>', unsafe_allow_html=True)

def analyze_with_ai(data_file, user_query):
    """Execute AI analysis"""
    with st.spinner("🤖 AI agents are analyzing your request..."):
        try:
            inputs = {
                'filename': data_file,
                'user_request': user_query,
            }
            
            result = Dataexp().crew().kickoff(inputs=inputs)
            
            # Display results
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.markdown("### 🎯 AI Analysis Results")
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Check for generated visualizations
            check_generated_files()
            
        except Exception as e:
            st.error(f"❌ AI analysis failed: {str(e)}")
            st.info("💡 Try using the Direct SQL Query mode instead.")

def execute_sql_query(data_file, sql_query):
    """Execute SQL query"""
    with st.spinner("⚡ Executing SQL query..."):
        try:
            result = execute_sql_on_csv.run(data_file, sql_query)
            result_data = json.loads(result)
            
            if "error" in result_data:
                st.error(f"❌ SQL Error: {result_data['error']}")
                return
            
            # Display results
            df = pd.DataFrame(result_data)
            
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.success(f"✅ Query executed successfully! ({len(df)} rows returned)")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Save results option
            if st.button("💾 Save Results"):
                save_query_results(result, sql_query)
            
            # Auto-generate visualization if suitable
            if len(df.columns) >= 1:
                create_visualization(df)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Query execution failed: {str(e)}")

def save_query_results(result, sql_query):
    """Save query results to file"""
    try:
        filename = f"query_result_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        save_result = save_dataframe(result, filename, "csv")
        save_data = json.loads(save_result)
        
        if "error" not in save_data:
            st.success(f"✅ Results saved to: {save_data['file_path']}")
        else:
            st.error(f"❌ Save failed: {save_data['error']}")
    except Exception as e:
        st.error(f"❌ Error saving results: {str(e)}")

def create_visualization(df):
    """Create visualization for query results"""
    st.markdown("### 📊 Data Visualization")
    
    if df.empty:
        st.warning("No data available for visualization.")
        return
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(numeric_cols) == 0 and len(categorical_cols) == 0:
        st.info("No suitable columns available for visualization.")
        return
    
    # Create columns for chart selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        available_charts = []
        
        # Determine available chart types based on data
        if categorical_cols and numeric_cols:
            available_charts.append("Bar Chart")
        if len(numeric_cols) >= 2:
            available_charts.extend(["Scatter Plot", "Line Chart"])
        if numeric_cols:
            available_charts.append("Histogram")
        if categorical_cols:
            available_charts.append("Count Plot")
        
        if not available_charts:
            st.info("No visualization types available for this data.")
            return
        
        viz_type = st.selectbox("Choose visualization type:", available_charts)
    
    with col2:
        try:
            if viz_type == "Bar Chart" and categorical_cols and numeric_cols:
                x_col = st.selectbox("X-axis (Category):", categorical_cols, key="bar_x")
                y_col = st.selectbox("Y-axis (Numeric):", numeric_cols, key="bar_y")
                
                if len(df) <= 100:  # Increased limit for better usability
                    fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                    fig.update_layout(
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Too many data points for bar chart. Consider filtering your data or try a different chart type.")
            
            elif viz_type == "Histogram" and numeric_cols:
                col = st.selectbox("Column:", numeric_cols, key="hist_col")
                bins = st.slider("Number of bins:", 10, 100, 30, key="hist_bins")
                
                fig = px.histogram(df, x=col, nbins=bins, title=f"Distribution of {col}")
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
                x_col = st.selectbox("X-axis:", numeric_cols, key="scatter_x")
                y_col = st.selectbox("Y-axis:", [col for col in numeric_cols if col != x_col], key="scatter_y")
                color_col = st.selectbox("Color by:", [None] + categorical_cols + numeric_cols, key="scatter_color")
                
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Line Chart" and len(numeric_cols) >= 2:
                x_col = st.selectbox("X-axis:", numeric_cols, key="line_x")
                y_col = st.selectbox("Y-axis:", [col for col in numeric_cols if col != x_col], key="line_y")
                
                # Sort by x-axis for better line chart
                df_sorted = df.sort_values(x_col)
                
                fig = px.line(df_sorted, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Count Plot" and categorical_cols:
                col = st.selectbox("Column:", categorical_cols, key="count_col")
                
                # Create count data
                count_data = df[col].value_counts().reset_index()
                count_data.columns = [col, 'count']
                
                fig = px.bar(count_data, x=col, y='count', title=f"Count of {col}")
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.info("Selected chart type is not available for the current data structure.")
                
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            st.info("💡 Try selecting different columns or chart types.")
            
            # Show debug information
            with st.expander("Debug Information"):
                st.write("DataFrame shape:", df.shape)
                st.write("Numeric columns:", numeric_cols)
                st.write("Categorical columns:", categorical_cols)
                st.write("DataFrame types:", df.dtypes.to_dict())

def check_generated_files():
    """Check for and display generated files from AI analysis"""
    try:
        output_dir = Path("output")
        if output_dir.exists():
            csv_files = list(output_dir.glob("*.csv"))
            if csv_files:
                st.markdown("### 📈 Generated Data Files")
                latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
                df = pd.read_csv(latest_file)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                if len(df.columns) >= 1:
                    create_visualization(df)
    except Exception as e:
        st.warning(f"Could not load generated files: {str(e)}")

if __name__ == "__main__":
    main()
