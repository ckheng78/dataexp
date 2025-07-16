# DataExp - Streamlit Web Interface

This guide shows how to use the Streamlit web interface with your CrewAI data exploration project.

## Installation

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -e .
   ```

2. **Install additional dependencies**:
   ```bash
   pip install streamlit plotly
   ```

## Running the Streamlit App

### Method 1: Direct Streamlit Command
```bash
streamlit run app.py
```

### Method 2: Using Python Script
```bash
python run_app.py
```

### Method 3: Using Project Script (after installation)
```bash
streamlit_app
```

## Features

### 🔧 Configuration Panel
- **Data Source Selection**: Upload your own CSV or use the Titanic dataset
- **CrewAI Integration**: Toggle between CrewAI agents and direct SQL execution

### 📋 Dataset Overview
- **Dataset Information**: View rows, columns, data types
- **Sample Data**: Preview your data
- **Missing Values**: Identify data quality issues

### 🔍 Data Analysis
- **CrewAI Analysis**: Natural language queries processed by AI agents
- **Direct SQL Queries**: Execute SQL directly on your data
- **Interactive Visualizations**: Auto-generated charts and graphs

### 📊 Data Visualization
- **Bar Charts**: Compare categorical data
- **Line Charts**: Show trends over time
- **Scatter Plots**: Explore relationships between variables
- **Histograms**: Understand data distributions

### 💾 Data Management
- **Save Results**: Export query results to CSV
- **Load Previous Results**: Import saved analyses
- **Session Management**: Cache frequently used data

## Usage Examples

### Example 1: Natural Language Query
1. Select "CrewAI Analysis" mode
2. Enter: "What is the survival rate by passenger class?"
3. Click "🚀 Analyze Data"
4. View AI-generated insights and visualizations

### Example 2: Direct SQL Query
1. Select "Direct SQL Query" mode
2. Enter: `SELECT Pclass, AVG(Age) as avg_age FROM df GROUP BY Pclass`
3. Click "🚀 Analyze Data"
4. View results and create visualizations

### Example 3: Upload Custom Data
1. Select "Upload File" in the sidebar
2. Upload your CSV file
3. View dataset overview
4. Perform analysis using either CrewAI or SQL

## File Structure

```
dataexp/
├── app.py                 # Main Streamlit application
├── run_app.py            # Streamlit launcher script
├── src/dataexp/
│   ├── main.py           # Updated with Streamlit integration
│   ├── crew.py           # CrewAI configuration
│   └── tools/
│       └── data_tool.py  # Data manipulation tools
└── output/               # Generated results (auto-created)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install streamlit plotly pandas
   ```

2. **File Not Found**: Ensure the Titanic dataset is in the correct location
   ```
   src/dataexp/data/titanic.csv
   ```

3. **CrewAI Errors**: Check that your CrewAI configuration is correct
   ```bash
   crewai run  # Test the crew separately
   ```

### Port Issues
If port 8501 is already in use, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## Advanced Features

### Custom SQL Functions
The app supports advanced SQL operations:
- Aggregations: `AVG()`, `COUNT()`, `SUM()`, `MAX()`, `MIN()`
- Filtering: `WHERE`, `HAVING`
- Grouping: `GROUP BY`
- Sorting: `ORDER BY`
- Joins: Not supported (single table only)

### Data Export Options
- **CSV**: Human-readable format
- **JSON**: Structured data format
- **Parquet**: Efficient columnar format
- **Pickle**: Python-specific format

### Visualization Customization
- **Chart Types**: Bar, Line, Scatter, Histogram
- **Color Coding**: Group by categorical variables
- **Interactive Features**: Zoom, pan, hover details

## Next Steps

1. **Extend the UI**: Add more visualization types
2. **Add Authentication**: Secure your app
3. **Deploy**: Use Streamlit Cloud or other hosting services
4. **Custom Themes**: Modify the CSS for branding

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify your data format matches expected CSV structure
3. Test CrewAI functionality separately using `crewai run`
