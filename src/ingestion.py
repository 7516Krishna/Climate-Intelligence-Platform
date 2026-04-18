import logging
from pathlib import Path
from typing import Dict

import pandas as pd


logger = logging.getLogger(__name__)


def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from CSV."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded from {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def validate_data(df: pd.DataFrame, config: Dict) -> None:
    """Validate required input columns and mapping choices."""
    required_cols = [
        config["columns"]["date"],
        config["columns"]["temperature"],
        config["columns"]["rainfall"],
    ]

    if len(set(required_cols)) != len(required_cols):
        logger.error("Date, temperature, and rainfall columns must be different")
        raise ValueError(
            "Date, temperature, and rainfall must be mapped to three different columns."
        )

    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        logger.error(f"Missing columns: {missing_cols}")
        raise ValueError(f"Missing columns: {missing_cols}")

    logger.info("Data validation successful")


def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """Save processed data to CSV."""
    try:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False)
        logger.info(f"Processed data saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise
