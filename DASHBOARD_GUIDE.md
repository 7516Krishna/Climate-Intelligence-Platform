# Climate Intelligence Dashboard - Quick Reference Guide

## 🌍 Overview

A modern SaaS-style **Climate Intelligence Dashboard** built with Streamlit and Plotly for advanced climate data analysis, featuring:
- Interactive CSV uploads with dynamic column mapping
- Full-pipeline climate analysis (preprocessing → forecasting)
- Real-time anomaly detection
- Beautiful dark theme with professional UI
- Exportable results and reports

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Virtual environment (venv)
- Required packages: streamlit, pandas, plotly, scikit-learn, statsmodels

### Installation & Launch

```bash
# Navigate to project directory
cd "C:\Users\Krishna Kadel\Climate-Intelligence-Platform"

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Launch dashboard
streamlit run dashboards/app.py
```

**Access Dashboard**: http://localhost:8503

---

## 📊 Dashboard Features

### 1. FILE UPLOAD & CONFIGURATION
**Section**: "📁 Data Upload & Configuration"

#### CSV File Upload
- Click file uploader to select climate data CSV
- Supports comma-separated values
- Displays success message with row/column count
- Shows preview of first 5 rows (expandable)

#### Column Mapping
**Required Selections**:
- **Date Column**: Select column containing dates/timestamps
- **Temperature Column**: Select column with temperature values
- **Rainfall Column**: Select column with rainfall measurements

#### Advanced Settings (Optional)
- **Anomaly Contamination Rate**: Expected proportion of anomalies (default: 1%)
- **Rolling Window**: Days for rolling calculations (default: 30)
- **Forecast Steps**: Number of periods to forecast (default: 30)

### 2. RUN ANALYSIS PIPELINE
**Button**: "🚀 Run Full Analysis Pipeline"

**Processing Steps**:
1. Data validation and cleaning
2. DateTime conversion and sorting
3. Forward-fill missing values
4. Time-based feature engineering (year, month, day, weekday)
5. Rolling statistics computation (30-day mean/std)
6. Isolation Forest anomaly detection
7. ARIMA time series forecasting

**Expected Duration**: 5-30 seconds depending on data size

---

## 📈 Analysis Results

### KPI Cards (Top Row)
Display key metrics in 4 cards:

| Metric | Description |
|--------|-------------|
| **Avg Temperature** | Mean temperature across dataset |
| **Max Temperature** | Highest temperature value |
| **Total Rainfall** | Sum of all rainfall measurements |
| **Anomalies Detected** | Count of detected anomalies |

### Visualization Tabs

#### 📊 Trend Tab
- **Line Chart**: Temperature over time
- **Overlay**: 30-day rolling mean (dashed yellow line)
- **Interaction**: Hover for values, zoom/pan available

#### 🚨 Anomaly Tab
- **Scatter Plot**: Blue dots = normal, Red diamonds = anomalies
- **Detection Method**: Isolation Forest algorithm
- **Threshold**: Configurable contamination rate

#### 🔮 Forecast Tab
- **Historical Data**: Blue line showing actual temperatures
- **Forecast Line**: Yellow dashed line for predicted values
- **Model**: ARIMA with automatic fallback order selection

#### 💧 Rainfall Tab
- **Bar Chart**: Daily/Period rainfall amounts
- **Color**: Blue bars for easy identification
- **Aggregation**: One bar per time period

#### 📅 Monthly Statistics Tab
- **Line Chart**: Average monthly temperatures
- **Shaded Area**: Min-max range per month
- **Aggregation**: Monthly statistics from entire dataset

### Data Tables

#### 📊 Summary Tab
Statistics overview including:
- Total records count
- Date range
- Temperature stats (mean, std, min, max)
- Rainfall stats (mean, std, total)
- Missing value count

#### 🚨 Anomalies Tab
- **Content**: All detected anomalies from dataset
- **Columns**: Date, Temperature, Rainfall, Rolling Mean
- **Display**: Up to 20 rows with scrolling
- **Status**: "No anomalies detected" if none found

#### 🔮 Forecast Tab
- **Content**: ARIMA forecast predictions
- **Columns**: Date, Forecast Value
- **Format**: Temperature values with 2 decimal precision

#### 📥 Processed Data Tab
- **Content**: Complete processed dataset
- **Format**: All columns including engineered features
- **Height**: Scrollable 400px view
- **Export**: Available via "Download Processed Data" button

---

## 💾 Export Options

### Download Processed Data
- **Format**: CSV file
- **Content**: Full processed dataset with all features
- **Size**: ~1-10MB depending on data size
- **Usage**: For external analysis or archival

### Download Analysis Report
- **Format**: Markdown (.md)
- **Content**: 
  - Dataset summary (rows, date range)
  - Temperature analysis (avg, min, max, std)
  - Rainfall analysis (total, average)
  - Anomaly statistics (count, percentage)
- **Usage**: Documentation, reports, presentations

---

## 🎨 UI Components

### Color Scheme (Dark Theme)
```
Background:      #071320  (Deep Navy)
Panels:          #0E1B2E  (Dark Blue)
Panel Alt:       #12243B  (Slightly Lighter Blue)
Primary Text:    #F4F7FB  (Off-White)
Secondary Text:  #9FB1CC  (Light Gray)
Accent Blue:     #6EC6FF  (Bright Blue)
Accent Yellow:   #FFD166  (Warm Yellow)
Accent Alert:    #FF6B7D  (Red)
```

### Layout
- **Width**: Wide layout (st.set_page_config)
- **Grid**: Responsive columns auto-adjust to screen
- **Spacing**: Consistent padding and margins
- **Typography**: Clean sans-serif fonts with hierarchy

---

## ⚙️ Technical Architecture

### Core Modules Used
- **Preprocessing** (`src/preprocessing.py`): Data cleaning, datetime conversion
- **Feature Engineering** (`src/feature_engineering.py`): Time features, rolling stats
- **Anomaly Detection** (`src/anomaly.py`): Isolation Forest implementation
- **Forecasting** (`src/forecasting.py`): ARIMA with fallback orders

### Data Flow
```
CSV Upload
    ↓
Column Mapping Selection
    ↓
Validation & Cleaning
    ↓
Time Feature Engineering
    ↓
Rolling Statistics
    ↓
Anomaly Detection
    ↓
ARIMA Forecasting
    ↓
Visualization & Tables
    ↓
Export Options
```

### Session State
- `st.session_state.df`: Processed DataFrame
- `st.session_state.config`: Configuration dictionary

---

## 🔧 Advanced Settings Explained

### Anomaly Contamination Rate
- **Range**: 0.1% to 10%
- **Default**: 1%
- **Interpretation**: Expected % of data points that are anomalies
- **Higher Values**: More anomalies detected
- **Use Case**: Adjust based on your expected anomaly frequency

### Rolling Window
- **Range**: 7 to 90 days
- **Default**: 30 days
- **Purpose**: Smooths data by averaging over period
- **Higher Values**: More smoothing, removes noise
- **Trade-off**: Loses detail vs. emphasizes trends

### Forecast Steps
- **Range**: 7 to 90 periods
- **Default**: 30
- **Purpose**: Number of future periods to predict
- **Calibration**: Based on ARIMA order and data availability
- **Limit**: Forecasts lose reliability beyond 3x historical range

---

## 📋 Example Workflow

### Scenario: Analyze Monthly Temperature Data

1. **Prepare Data**
   - Ensure CSV has columns: Date, Avg_Temp, Total_Rain
   - Format dates as YYYY-MM-DD or YYYY-MM-01

2. **Upload**
   - Click "Upload Climate CSV"
   - Select your CSV file
   - Review preview

3. **Configure**
   - Select Date Column: "Date"
   - Select Temperature Column: "Avg_Temp"
   - Select Rainfall Column: "Total_Rain"
   - Keep other settings default or adjust as needed

4. **Run Analysis**
   - Click "🚀 Run Full Analysis Pipeline"
   - Wait for completion (green checkmark appears)

5. **Explore Results**
   - View KPI cards at top
   - Click through visualization tabs
   - Review summary statistics
   - Check for detected anomalies

6. **Export**
   - Download processed CSV for spreadsheet analysis
   - Download markdown report for documentation
   - Share visualizations (Plotly native export via chart menu)

---

## ⚠️ Troubleshooting

### Issue: App won't start
**Solution**: Verify virtual environment is activated and streamlit is installed
```bash
pip list | grep streamlit
```

### Issue: Column mapping dropdown empty
**Solution**: Ensure CSV is properly formatted with readable headers

### Issue: Pipeline fails with "No anomalies detected"
**Resolution**: This is normal! Some datasets have no outliers. This is a success message.

### Issue: Forecasting not working
**Workaround**: Try increasing forecast steps or reducing ARIMA order in advanced settings

### Issue: Large CSV takes too long
**Optimization**: 
- Reduce dataset size (sample rows)
- Increase rolling window
- Use simpler ARIMA orders

---

## 🎯 Best Practices

1. **Data Quality**
   - Ensure Date column is properly formatted
   - Remove header rows in raw data
   - Handle missing values before upload if possible

2. **Column Selection**
   - Use date format YYYY-MM-DD or YYYY-MM-01
   - Select numeric columns for temperature and rainfall
   - Verify column names are clear

3. **Analysis Settings**
   - Start with defaults
   - Adjust contamination rate to match expected anomalies
   - Increase forecast steps cautiously

4. **Result Interpretation**
   - Anomalies = Deviation from normal pattern
   - Forecast = Trend continuation (limited reliability)
   - Rolling mean = General trend direction

---

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python
- **ARIMA Guide**: https://www.statsmodels.org/stable/tsa_arima.html
- **Anomaly Detection**: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html

---

## ✨ Feature Roadmap

Potential future enhancements:
- [ ] Seasonal decomposition charts
- [ ] Custom alert threshold configuration
- [ ] Real-time data streaming
- [ ] Multi-file batch analysis
- [ ] Correlation matrix heatmaps
- [ ] Statistical hypothesis tests
- [ ] Model performance metrics display
- [ ] Download forecast as CSV

---

**Dashboard Version**: 1.0  
**Last Updated**: April 2026  
**Status**: Production Ready ✅
