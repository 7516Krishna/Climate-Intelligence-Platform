import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def preprocess_data(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Clean and preprocess climate data"""

    try:
        df = df.copy()
        date_col = config["columns"]["date"]
        temp_col = config["columns"]["temperature"]
        rain_col = config["columns"]["rainfall"]

        # Validate columns exist
        missing_cols = [c for c in [date_col, temp_col, rain_col] if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {', '.join(missing_cols)}. Available columns: {', '.join(df.columns)}")

        # Convert to datetime
        df[date_col] = pd.to_datetime(df[date_col].astype(str).str.strip(), format=None, errors="coerce")
        df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")
        df[rain_col] = pd.to_numeric(df[rain_col], errors="coerce")

        # Check if we have any valid dates
        valid_dates = df[date_col].notna().sum()
        if valid_dates == 0:
            raise ValueError(f"Column '{date_col}' contains no valid dates. Please verify you selected the correct date column.")

        # Drop invalid dates
        df = df.dropna(subset=[date_col])
        
        if len(df) == 0:
            raise ValueError("No valid date values found after filtering.")

        # Sort by date and keep the most recent row for duplicate dates
        df = df.sort_values(by=date_col).drop_duplicates(subset=[date_col], keep="last")

        # Ensure numeric columns exist and have valid data
        valid_temps = df[temp_col].notna().sum()
        valid_rains = df[rain_col].notna().sum()
        
        if valid_temps == 0:
            raise ValueError(f"Column '{temp_col}' contains no valid numeric temperature values.")
        if valid_rains == 0:
            raise ValueError(f"Column '{rain_col}' contains no valid numeric rainfall values.")

        # Handle missing values
        fill_method = config["preprocessing"]["fill_method"]

        if fill_method == "ffill":
            df = df.ffill()
        elif fill_method == "bfill":
            df = df.bfill()
        else:
            raise ValueError(
                "Unsupported fill_method. Use 'ffill' or 'bfill' in config/config.yaml."
            )

        # Downstream analysis requires at least a numeric temperature signal.
        df = df.dropna(subset=[temp_col]).reset_index(drop=True)
        
        if len(df) == 0:
            raise ValueError("No valid temperature values remain after preprocessing.")

        logger.info("Preprocessing completed successfully")

        return df

    except Exception as e:
        logger.error(f"Preprocessing failed: {e}")
        raise
    
