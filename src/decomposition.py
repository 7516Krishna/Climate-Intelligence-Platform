import logging
import pandas as pd
from typing import Dict, Any
from statsmodels.tsa.seasonal import seasonal_decompose

logger = logging.getLogger(__name__)


def decompose_time_series(df: pd.DataFrame, config: Dict) -> Dict[str, Any]:
    """
    Perform robust seasonal decomposition on temperature time series.

    Returns:
        dict with keys:
        - trend
        - seasonal
        - residual
        - observed
    """

    try:
        date_col = config["columns"]["date"]
        temp_col = config["columns"]["temperature"]

        # =========================
        # 1. VALIDATION
        # =========================
        if date_col not in df.columns or temp_col not in df.columns:
            raise ValueError("Required columns missing for decomposition")

        # =========================
        # 2. PREPARE TIME SERIES
        # =========================
        df = df.copy()

        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")
        df = df.dropna(subset=[date_col])

        df = df.sort_values(by=date_col)
        df = df.set_index(date_col)
        df = df.groupby(level=0)[temp_col].mean().to_frame()

        # Ensure daily frequency
        df = df.asfreq("D")

        # =========================
        # 3. HANDLE MISSING VALUES
        # =========================
        df[temp_col] = df[temp_col].interpolate(method="linear")
        df = df.dropna(subset=[temp_col])

        # =========================
        # 4. AUTO PERIOD SELECTION
        # =========================
        data_length = len(df)

        if data_length >= 730:
            period = 365  # yearly seasonality
        elif data_length >= 180:
            period = 30   # monthly seasonality
        else:
            logger.warning("Data too short for meaningful decomposition")
            return {}

        logger.info(f"Using decomposition period: {period}")

        # =========================
        # 5. DECOMPOSITION
        # =========================
        result = seasonal_decompose(
            df[temp_col],
            model="additive",
            period=period,
            extrapolate_trend="freq",
        )

        logger.info("Decomposition completed successfully")

        return {
            "trend": result.trend,
            "seasonal": result.seasonal,
            "residual": result.resid,
            "observed": result.observed
        }

    except Exception as e:
        logger.error(f"Decomposition failed: {e}")
        raise
