import logging
import pandas as pd
from typing import Dict
from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)


def detect_anomalies(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """
    Detect anomalies using Isolation Forest
    """

    try:
        df = df.copy()
        temp_col = config["columns"]["temperature"]
        contamination = float(config["anomaly"]["contamination"])
        temperature_values = (
            pd.to_numeric(df[temp_col], errors="coerce")
            .interpolate(limit_direction="both")
        )

        df["anomaly"] = 0

        valid_mask = temperature_values.notna()
        valid_count = int(valid_mask.sum())

        if valid_count < 2:
            logger.warning("Skipping anomaly detection: at least two temperature values are required")
            return df

        contamination = min(max(contamination, 1 / valid_count), 0.5)

        model = IsolationForest(
            contamination=contamination,
            random_state=42
        )

        predictions = model.fit_predict(temperature_values[valid_mask].to_frame(name=temp_col))

        # Convert output: -1 = anomaly, 1 = normal
        df.loc[valid_mask, "anomaly"] = (predictions == -1).astype(int)

        logger.info("Anomaly detection completed")

        return df

    except Exception as e:
        logger.error(f"Anomaly detection failed: {e}")
        raise
