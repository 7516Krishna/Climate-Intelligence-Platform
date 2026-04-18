import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def create_time_features(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Create time-based features"""

    try:
        date_col = config["columns"]["date"]
        
        # Ensure date column is datetime type
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

        df["year"] = df[date_col].dt.year
        df["month"] = df[date_col].dt.month
        df["day"] = df[date_col].dt.day
        df["dayofweek"] = df[date_col].dt.dayofweek

        logger.info("Time features created")

        return df

    except Exception as e:
        logger.error(f"Feature engineering failed: {e}")
        raise


def create_rolling_features(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Create rolling statistics"""

    try:
        window = config["features"]["rolling_window"]
        temp_col = config["columns"]["temperature"]

        df = df.copy()
        
        # Validate column exists and has numeric data
        if temp_col not in df.columns:
            raise ValueError(f"Temperature column '{temp_col}' not found in dataframe.")
        
        # Ensure column is numeric
        if not pd.api.types.is_numeric_dtype(df[temp_col]):
            df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")
        
        # Check if we have any data to work with
        valid_count = df[temp_col].notna().sum()
        if valid_count == 0:
            raise ValueError(f"No valid numeric values in temperature column '{temp_col}'.")
        
        df["temp_rolling_mean"] = df[temp_col].rolling(window=window, min_periods=1).mean()
        df["temp_rolling_std"] = (
            df[temp_col].rolling(window=window, min_periods=1).std().fillna(0.0)
        )

        logger.info("Rolling features created")

        return df

    except Exception as e:
        logger.error(f"Rolling feature creation failed: {e}")
        raise
