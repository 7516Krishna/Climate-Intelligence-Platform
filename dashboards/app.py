from __future__ import annotations

import io

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


PAGE_BACKGROUND = "#071320"
PANEL_BACKGROUND = "#0E1B2E"
PANEL_BACKGROUND_ALT = "#12243B"
BORDER_COLOR = "rgba(150, 180, 255, 0.14)"
TEXT_PRIMARY = "#F4F7FB"
TEXT_SECONDARY = "#9FB1CC"
ACCENT_BLUE = "#6EC6FF"
ACCENT_ORANGE = "#FF9F43"
ACCENT_RED = "#FF5A6E"
ACCENT_GREEN = "#42D392"
ACCENT_YELLOW = "#FFD166"


def apply_dashboard_styles() -> None:
    """Apply a dark SaaS-style theme to the Streamlit dashboard."""
    st.markdown(
        f"""
        <style>
        :root {{
            --page-bg: {PAGE_BACKGROUND};
            --panel-bg: {PANEL_BACKGROUND};
            --panel-bg-alt: {PANEL_BACKGROUND_ALT};
            --border-color: {BORDER_COLOR};
            --text-primary: {TEXT_PRIMARY};
            --text-secondary: {TEXT_SECONDARY};
            --accent-blue: {ACCENT_BLUE};
            --accent-orange: {ACCENT_ORANGE};
            --accent-red: {ACCENT_RED};
            --accent-green: {ACCENT_GREEN};
            --accent-yellow: {ACCENT_YELLOW};
        }}

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stSidebar"] {{
            background: var(--page-bg);
            color: var(--text-primary);
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1400px;
        }}

        h1, h2, h3, h4, h5, h6, label {{
            color: var(--text-primary);
        }}

        p, li, small {{
            color: var(--text-secondary);
        }}

        [data-testid="stFileUploaderDropzone"] {{
            background: linear-gradient(180deg, var(--panel-bg-alt) 0%, var(--panel-bg) 100%);
            border: 1px dashed rgba(110, 198, 255, 0.28);
            border-radius: 18px;
        }}

        [data-baseweb="select"] > div,
        [data-testid="stNumberInputContainer"] > div,
        [data-testid="stTextInputRootElement"] {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            color: var(--text-primary);
        }}

        [role="listbox"] {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
        }}

        [role="option"] {{
            background: var(--panel-bg);
            color: var(--text-primary);
        }}

        [role="option"][aria-selected="true"] {{
            background: rgba(110, 198, 255, 0.12);
        }}

        [data-testid="stMetric"] {{
            background: linear-gradient(180deg, var(--panel-bg-alt) 0%, var(--panel-bg) 100%);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.05rem 1rem;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.28);
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--text-primary);
            font-size: 2rem;
            font-weight: 700;
        }}

        [data-testid="stMetricDelta"] {{
            color: var(--accent-blue);
        }}

        div[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
            > div[data-testid="column"]:last-child [data-testid="stMetric"] {{
            border: 1px solid rgba(255, 90, 110, 0.65);
            box-shadow: 0 0 0 1px rgba(255, 90, 110, 0.14), 0 18px 40px rgba(0, 0, 0, 0.28);
        }}

        [data-testid="stPlotlyChart"],
        [data-testid="stDataFrame"] {{
            background: linear-gradient(180deg, var(--panel-bg-alt) 0%, var(--panel-bg) 100%);
            border: 1px solid var(--border-color);
            border-radius: 22px;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.26);
            padding: 0.45rem 0.8rem 0.75rem 0.8rem;
        }}

        .stButton > button,
        [data-testid="baseButton-secondary"] {{
            background: linear-gradient(135deg, var(--accent-blue) 0%, #4F9EDB 100%);
            color: #04101D;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            box-shadow: 0 14px 30px rgba(110, 198, 255, 0.22);
        }}

        .hero-card,
        .panel-card {{
            background: linear-gradient(180deg, var(--panel-bg-alt) 0%, var(--panel-bg) 100%);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.24);
            padding: 1.25rem 1.35rem;
        }}

        .hero-card {{
            background:
                radial-gradient(circle at top left, rgba(110, 198, 255, 0.18), transparent 32%),
                linear-gradient(180deg, #12243B 0%, #0B1728 100%);
        }}

        .eyebrow {{
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--accent-blue);
            margin-bottom: 0.75rem;
        }}

        .hero-title {{
            margin: 0;
            font-size: 2.15rem;
            font-weight: 800;
            color: var(--text-primary);
        }}

        .hero-copy {{
            margin-top: 0.75rem;
            line-height: 1.65;
            color: var(--text-secondary);
        }}

        .panel-title {{
            margin: 0;
            font-size: 1.04rem;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .panel-subtitle {{
            margin: 0.35rem 0 0 0;
            color: var(--text-secondary);
            font-size: 0.92rem;
        }}

        .insight-list {{
            margin: 0.9rem 0 0 0;
            padding-left: 1.1rem;
        }}

        .insight-list li {{
            margin-bottom: 0.6rem;
            line-height: 1.55;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def configure_page() -> None:
    """Configure the Streamlit page."""
    st.set_page_config(page_title="Climate Intelligence Dashboard", layout="wide")
    apply_dashboard_styles()


def initialize_session_state() -> None:
    """Initialize state used across Streamlit reruns."""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "uploaded_signature" not in st.session_state:
        st.session_state.uploaded_signature = None


def create_config_from_mapping(
    date_col: str,
    temp_col: str,
    rain_col: str,
    rolling_window: int = 30,
    forecast_steps: int = 30,
    anomaly_zscore: float = 2.5,
) -> dict:
    """Build a lightweight dashboard config from the selected column mapping."""
    return {
        "columns": {
            "date": date_col,
            "temperature": temp_col,
            "rainfall": rain_col,
        },
        "features": {
            "rolling_window": rolling_window,
        },
        "forecast": {
            "steps": forecast_steps,
        },
        "anomaly": {
            "zscore_threshold": anomaly_zscore,
        },
    }


def infer_default_columns(columns: list[str]) -> dict[str, str]:
    """Infer sensible column defaults from common climate naming patterns."""
    lowered = {column: column.lower().replace("_", " ").replace("-", " ") for column in columns}

    def find_match(keywords: tuple[str, ...], excluded: set[str]) -> str | None:
        for keyword in keywords:
            for column in columns:
                if column not in excluded and keyword in lowered[column]:
                    return column
        return None

    selected: dict[str, str] = {}
    selected["date"] = find_match(("date", "time", "timestamp", "year"), set()) or columns[0]
    selected["temperature"] = find_match(
        ("temperature", "temp", "tmax", "tmin", "tavg"),
        {selected["date"]},
    ) or next((column for column in columns if column != selected["date"]), columns[0])
    selected["rainfall"] = find_match(
        ("rainfall", "rain", "prcp", "precip"),
        {selected["date"], selected["temperature"]},
    ) or next(
        (
            column
            for column in columns
            if column not in {selected["date"], selected["temperature"]}
        ),
        columns[0],
    )
    return selected


def get_default_index(columns: list[str], selected_column: str) -> int:
    """Resolve the default selectbox index for a column name."""
    return columns.index(selected_column) if selected_column in columns else 0


def load_uploaded_csv(uploaded_file) -> pd.DataFrame:
    """Read the uploaded CSV file into a DataFrame."""
    file_bytes = uploaded_file.getvalue()
    return pd.read_csv(io.BytesIO(file_bytes))


def preprocess_uploaded_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Clean and feature-engineer uploaded climate data."""
    date_col = config["columns"]["date"]
    temp_col = config["columns"]["temperature"]
    rain_col = config["columns"]["rainfall"]

    if len({date_col, temp_col, rain_col}) != 3:
        raise ValueError("Date, temperature, and rainfall must be mapped to three different columns.")

    missing_cols = [column for column in (date_col, temp_col, rain_col) if column not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {', '.join(missing_cols)}")

    processed_df = df.copy()
    processed_df[date_col] = pd.to_datetime(
        processed_df[date_col].astype(str).str.strip(),
        errors="coerce",
    )
    processed_df[temp_col] = pd.to_numeric(processed_df[temp_col], errors="coerce")
    processed_df[rain_col] = pd.to_numeric(processed_df[rain_col], errors="coerce")

    processed_df = processed_df.dropna(subset=[date_col]).sort_values(by=date_col)
    processed_df = processed_df.drop_duplicates(subset=[date_col], keep="last")

    if processed_df.empty:
        raise ValueError("No valid date values were found after parsing the selected date column.")

    processed_df[[temp_col, rain_col]] = processed_df[[temp_col, rain_col]].ffill().bfill()
    processed_df = processed_df.dropna(subset=[temp_col, rain_col]).reset_index(drop=True)

    if processed_df.empty:
        raise ValueError("No valid numeric temperature and rainfall values remain after preprocessing.")

    rolling_window = min(int(config["features"]["rolling_window"]), len(processed_df))
    processed_df["year"] = processed_df[date_col].dt.year
    processed_df["month"] = processed_df[date_col].dt.month
    processed_df["temp_rolling_mean"] = processed_df[temp_col].rolling(
        window=max(rolling_window, 1),
        min_periods=1,
    ).mean()

    return processed_df


def add_anomaly_flags(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Add anomaly flags using a simple z-score approach."""
    processed_df = df.copy()
    temp_col = config["columns"]["temperature"]
    threshold = float(config["anomaly"]["zscore_threshold"])

    temperature = processed_df[temp_col].astype(float)
    std = temperature.std(ddof=0)

    if pd.isna(std) or std == 0:
        processed_df["zscore"] = 0.0
        processed_df["anomaly"] = 0
        return processed_df

    processed_df["zscore"] = (temperature - temperature.mean()) / std
    processed_df["anomaly"] = (processed_df["zscore"].abs() >= threshold).astype(int)
    return processed_df


def build_forecast(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Create a simple 30-step forecast using a linear trend blended with the rolling mean."""
    date_col = config["columns"]["date"]
    temp_col = config["columns"]["temperature"]
    steps = int(config["forecast"]["steps"])

    working_df = df[[date_col, temp_col, "temp_rolling_mean"]].dropna().copy()
    if working_df.empty:
        raise ValueError("Forecasting requires at least one valid temperature observation.")

    first_date = working_df[date_col].min()
    last_date = working_df[date_col].max()
    day_index = (working_df[date_col] - first_date).dt.days.astype(float).to_numpy()
    temperature = working_df[temp_col].astype(float).to_numpy()

    if len(np.unique(day_index)) >= 2:
        slope, intercept = np.polyfit(day_index, temperature, 1)
        future_index = np.arange(day_index.max() + 1, day_index.max() + steps + 1)
        trend_values = slope * future_index + intercept
    else:
        trend_values = np.repeat(float(temperature[-1]), steps)

    baseline = float(working_df["temp_rolling_mean"].iloc[-1])
    forecast_values = 0.65 * trend_values + 0.35 * baseline

    forecast_df = pd.DataFrame(
        {
            date_col: pd.date_range(last_date + pd.Timedelta(days=1), periods=steps, freq="D"),
            "forecast_temperature": forecast_values,
        }
    )
    return forecast_df


def validate_and_process(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run the full climate dashboard pipeline and return processed + forecast data."""
    processed_df = preprocess_uploaded_data(df, config)
    processed_df = add_anomaly_flags(processed_df, config)
    forecast_df = build_forecast(processed_df, config)
    return processed_df, forecast_df


def filter_display_window(df: pd.DataFrame, date_col: str, selected_window: str) -> pd.DataFrame:
    """Filter processed data for the selected dashboard time window."""
    if selected_window == "All data":
        return df

    days_lookup = {
        "Last 30 days": 30,
        "Last 90 days": 90,
        "Last 180 days": 180,
    }
    cutoff = df[date_col].max() - pd.Timedelta(days=days_lookup[selected_window] - 1)
    filtered_df = df[df[date_col] >= cutoff]
    return filtered_df if not filtered_df.empty else df


def build_plotly_layout(title: str, yaxis_title: str) -> dict:
    """Shared Plotly dark-theme layout settings."""
    return {
        "title": title,
        "template": "plotly_dark",
        "paper_bgcolor": PANEL_BACKGROUND,
        "plot_bgcolor": PANEL_BACKGROUND,
        "font": {"color": TEXT_PRIMARY},
        "hovermode": "x unified",
        "margin": {"l": 20, "r": 20, "t": 56, "b": 18},
        "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
        "yaxis_title": yaxis_title,
        "xaxis_title": "Date",
    }


def build_trend_chart(df: pd.DataFrame, config: dict) -> go.Figure:
    """Build the temperature trend chart."""
    date_col = config["columns"]["date"]
    temp_col = config["columns"]["temperature"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[date_col],
            y=df[temp_col],
            mode="lines",
            name="Temperature",
            line={"color": ACCENT_BLUE, "width": 3},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[date_col],
            y=df["temp_rolling_mean"],
            mode="lines",
            name="30-day rolling mean",
            line={"color": ACCENT_YELLOW, "width": 2, "dash": "dash"},
        )
    )
    fig.update_layout(**build_plotly_layout("Temperature Trend", "Temperature"))
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


def build_anomaly_chart(df: pd.DataFrame, config: dict) -> go.Figure:
    """Build the anomaly detection chart."""
    date_col = config["columns"]["date"]
    temp_col = config["columns"]["temperature"]
    normal_df = df[df["anomaly"] == 0]
    anomaly_df = df[df["anomaly"] == 1]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=normal_df[date_col],
            y=normal_df[temp_col],
            mode="lines+markers",
            name="Temperature",
            line={"color": ACCENT_BLUE, "width": 2},
            marker={"size": 5},
        )
    )
    if not anomaly_df.empty:
        fig.add_trace(
            go.Scatter(
                x=anomaly_df[date_col],
                y=anomaly_df[temp_col],
                mode="markers",
                name="Anomaly",
                marker={"color": ACCENT_RED, "size": 9, "symbol": "diamond"},
            )
        )
    fig.update_layout(**build_plotly_layout("Anomaly Detection", "Temperature"))
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


def build_forecast_chart(history_df: pd.DataFrame, forecast_df: pd.DataFrame, config: dict) -> go.Figure:
    """Build the forecast chart."""
    date_col = config["columns"]["date"]
    temp_col = config["columns"]["temperature"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=history_df[date_col],
            y=history_df[temp_col],
            mode="lines",
            name="Historical",
            line={"color": ACCENT_BLUE, "width": 3},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df[date_col],
            y=forecast_df["forecast_temperature"],
            mode="lines",
            name="Forecast",
            line={"color": ACCENT_ORANGE, "width": 3},
        )
    )
    fig.update_layout(**build_plotly_layout("30-Step Forecast", "Temperature"))
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


def compute_kpis(df: pd.DataFrame, config: dict) -> list[tuple[str, str, str | None]]:
    """Compute KPI card values for the processed data."""
    temp_col = config["columns"]["temperature"]
    rain_col = config["columns"]["rainfall"]
    anomaly_count = int(df["anomaly"].sum())

    return [
        ("Avg Temperature", f"{df[temp_col].mean():.2f}", "Stable trend"),
        ("Max Temperature", f"{df[temp_col].max():.2f}", "Peak in range"),
        ("Total Rainfall", f"{df[rain_col].sum():.2f}", "Accumulated total"),
        ("Anomalies", str(anomaly_count), "Check alert rows"),
        ("Records", f"{len(df):,}", "Rows analyzed"),
    ]


def build_summary_table(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Build a compact summary table for the uploaded dataset."""
    date_col = config["columns"]["date"]
    temp_col = config["columns"]["temperature"]
    rain_col = config["columns"]["rainfall"]

    return pd.DataFrame(
        [
            {"Metric": "Rows analyzed", "Value": len(df)},
            {"Metric": "Date range", "Value": f"{df[date_col].min().date()} to {df[date_col].max().date()}"},
            {"Metric": "Average temperature", "Value": f"{df[temp_col].mean():.2f}"},
            {"Metric": "Max temperature", "Value": f"{df[temp_col].max():.2f}"},
            {"Metric": "Total rainfall", "Value": f"{df[rain_col].sum():.2f}"},
            {"Metric": "Anomaly count", "Value": int(df['anomaly'].sum())},
        ]
    )


def build_insights(df: pd.DataFrame, forecast_df: pd.DataFrame, config: dict) -> list[str]:
    """Generate simple narrative insights from the processed dataset."""
    temp_col = config["columns"]["temperature"]
    rain_col = config["columns"]["rainfall"]

    latest_temp = float(df[temp_col].iloc[-1])
    avg_temp = float(df[temp_col].mean())
    forecast_mean = float(forecast_df["forecast_temperature"].mean())
    anomaly_count = int(df["anomaly"].sum())

    insights = [
        f"Latest observed temperature is {latest_temp:.2f}, compared with an average of {avg_temp:.2f}.",
        f"Total rainfall in the filtered view is {df[rain_col].sum():.2f}, with {anomaly_count} anomaly points flagged.",
        f"The next {len(forecast_df)} forecasted periods average {forecast_mean:.2f}, providing a simple forward trend view.",
    ]
    return insights


def render_panel_header(title: str, subtitle: str) -> None:
    """Render a reusable panel heading."""
    st.markdown(
        f"""
        <div class="panel-card" style="margin-bottom: 0.85rem;">
            <h3 class="panel-title">{title}</h3>
            <p class="panel-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_table(title: str, subtitle: str, table_df: pd.DataFrame) -> None:
    """Render a styled dataframe panel."""
    render_panel_header(title, subtitle)
    st.dataframe(table_df, use_container_width=True, hide_index=True)


def render_insight_panel(insights: list[str]) -> None:
    """Render the narrative insights panel."""
    items = "".join(f"<li>{insight}</li>" for insight in insights)
    st.markdown(
        f"""
        <div class="panel-card">
            <h3 class="panel-title">Climate Insights</h3>
            <p class="panel-subtitle">Quick observations derived from the uploaded dataset.</p>
            <ul class="insight-list">{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def reset_analysis_if_new_file(uploaded_file) -> None:
    """Reset stored analysis when a different file is uploaded."""
    current_signature = (uploaded_file.name, getattr(uploaded_file, "size", None))
    if st.session_state.uploaded_signature != current_signature:
        st.session_state.analysis_result = None
        st.session_state.uploaded_signature = current_signature


def main() -> None:
    """Render the Climate Intelligence Dashboard."""
    configure_page()
    initialize_session_state()

    header_col, filter_col = st.columns([3.2, 1.4], gap="large")

    with header_col:
        st.markdown(
            """
            <div class="hero-card">
                <div class="eyebrow">Climate operations workspace</div>
                <h1 class="hero-title">Climate Intelligence Dashboard</h1>
                <p class="hero-copy">
                    Upload a climate CSV, map the core columns, and run a full analysis workflow with
                    trend monitoring, anomaly detection, and a lightweight forecast in one dark-mode
                    analytics surface.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    analysis_available = st.session_state.analysis_result is not None

    with filter_col:
        st.markdown(
            """
            <div class="panel-card">
                <h3 class="panel-title">Display filter</h3>
                <p class="panel-subtitle">Change the visible time window for charts and summary panels.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        display_window = st.selectbox(
            "Time range",
            ("All data", "Last 30 days", "Last 90 days", "Last 180 days"),
            disabled=not analysis_available,
        )

    upload_col, preview_col = st.columns([1.35, 1.65], gap="large")

    with upload_col:
        render_panel_header("Upload Climate CSV", "Bring your own climate dataset to run the dashboard pipeline.")
        uploaded_file = st.file_uploader("Upload Climate CSV", type=["csv"])

        if uploaded_file is None:
            st.info("Upload a CSV file to unlock the full analysis workflow.")
            return

        reset_analysis_if_new_file(uploaded_file)

        try:
            raw_df = load_uploaded_csv(uploaded_file)
        except Exception as error:
            st.error(f"Unable to read the uploaded CSV: {error}")
            return

        st.caption(f"{uploaded_file.name} loaded with {len(raw_df):,} rows and {len(raw_df.columns)} columns.")

        default_columns = infer_default_columns(raw_df.columns.tolist())

        date_col = st.selectbox(
            "Select Date Column",
            raw_df.columns,
            index=get_default_index(raw_df.columns.tolist(), default_columns["date"]),
        )
        temp_col = st.selectbox(
            "Select Temperature Column",
            raw_df.columns,
            index=get_default_index(raw_df.columns.tolist(), default_columns["temperature"]),
        )
        rain_col = st.selectbox(
            "Select Rainfall Column",
            raw_df.columns,
            index=get_default_index(raw_df.columns.tolist(), default_columns["rainfall"]),
        )

        setting_col_1, setting_col_2 = st.columns(2, gap="small")
        with setting_col_1:
            rolling_window = st.number_input("Rolling window", min_value=3, max_value=90, value=30)
        with setting_col_2:
            forecast_steps = st.number_input("Forecast steps", min_value=7, max_value=90, value=30)

        mapping_is_valid = len({date_col, temp_col, rain_col}) == 3
        if not mapping_is_valid:
            st.warning("Date, temperature, and rainfall must be mapped to three different columns.")

        run_analysis = st.button(
            "Run Climate Analysis",
            disabled=not mapping_is_valid,
            use_container_width=True,
        )

        if run_analysis:
            config = create_config_from_mapping(
                date_col=date_col,
                temp_col=temp_col,
                rain_col=rain_col,
                rolling_window=int(rolling_window),
                forecast_steps=int(forecast_steps),
            )
            try:
                with st.spinner("Running climate analysis pipeline..."):
                    processed_df, forecast_df = validate_and_process(raw_df, config)
                st.session_state.analysis_result = {
                    "raw_df": raw_df,
                    "processed_df": processed_df,
                    "forecast_df": forecast_df,
                    "config": config,
                }
                st.success("Analysis completed successfully.")
            except Exception as error:
                st.session_state.analysis_result = None
                st.error(f"Analysis failed: {error}")

    with preview_col:
        render_panel_header("Uploaded Data Preview", "First five rows from the uploaded climate dataset.")
        st.dataframe(raw_df.head(), use_container_width=True, hide_index=True)

    if st.session_state.analysis_result is None:
        return

    processed_df = st.session_state.analysis_result["processed_df"]
    forecast_df = st.session_state.analysis_result["forecast_df"]
    config = st.session_state.analysis_result["config"]
    date_col = config["columns"]["date"]

    filtered_df = filter_display_window(processed_df, date_col, display_window)
    insights = build_insights(filtered_df, forecast_df, config)

    metric_columns = st.columns(5, gap="medium")
    for column, (label, value, delta) in zip(metric_columns, compute_kpis(filtered_df, config)):
        column.metric(label, value, delta)

    chart_left, chart_right = st.columns([1.55, 1], gap="large")
    with chart_left:
        render_panel_header("Temperature Trend", "Historical observations with a rolling mean overlay.")
        st.plotly_chart(build_trend_chart(filtered_df, config), use_container_width=True)

    with chart_right:
        render_insight_panel(insights)

    anomaly_col, forecast_col = st.columns(2, gap="large")
    with anomaly_col:
        render_panel_header("Anomaly Detection", "Temperature anomalies highlighted in red using a z-score rule.")
        st.plotly_chart(build_anomaly_chart(filtered_df, config), use_container_width=True)

    with forecast_col:
        render_panel_header("Forecast", "Simple forward projection for the next 30 periods.")
        st.plotly_chart(build_forecast_chart(filtered_df, forecast_df, config), use_container_width=True)

    table_col_1, table_col_2, table_col_3 = st.columns(3, gap="large")
    with table_col_1:
        render_table(
            "Data Summary",
            "High-level metrics derived from the filtered view.",
            build_summary_table(filtered_df, config),
        )

    with table_col_2:
        anomaly_table = filtered_df.loc[filtered_df["anomaly"] == 1, [date_col, config["columns"]["temperature"], config["columns"]["rainfall"], "zscore"]]
        if anomaly_table.empty:
            anomaly_table = pd.DataFrame([{"Status": "No anomalies found in the selected time range."}])
        render_table(
            "Anomaly Table",
            "Rows flagged as unusual by the anomaly detector.",
            anomaly_table.head(20),
        )

    with table_col_3:
        render_table(
            "Forecast Table",
            "Forward-looking temperature estimates for the next periods.",
            forecast_df.head(30),
        )

    export_col_1, export_col_2 = st.columns(2, gap="large")
    with export_col_1:
        st.download_button(
            "Download Processed CSV",
            data=processed_df.to_csv(index=False),
            file_name="climate_analysis_results.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with export_col_2:
        st.download_button(
            "Download Forecast CSV",
            data=forecast_df.to_csv(index=False),
            file_name="climate_forecast.csv",
            mime="text/csv",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
