import logging
import warnings

import pandas as pd
from typing import Dict
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.sm_exceptions import ConvergenceWarning

logger = logging.getLogger(__name__)


def _minimum_observations(order: tuple[int, int, int]) -> int:
    """Estimate the minimum number of observations needed for the chosen ARIMA order."""
    return max(order[0], order[2]) + order[1] + 2


def _candidate_orders(primary_order: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """Return a prioritized list of ARIMA orders to try."""
    candidates = [
        primary_order,
        (2, 1, 0),
        (1, 1, 0),
        (1, 0, 0),
        (0, 1, 0),
    ]

    unique_candidates: list[tuple[int, int, int]] = []
    for candidate in candidates:
        if candidate not in unique_candidates:
            unique_candidates.append(candidate)

    return unique_candidates


def _fit_arima_with_fallback(series: pd.Series, primary_order: tuple[int, int, int]):
    """Fit ARIMA, falling back to simpler orders when convergence fails."""
    last_error: Exception | None = None

    for candidate_order in _candidate_orders(primary_order):
        if len(series) < _minimum_observations(candidate_order):
            continue

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", ConvergenceWarning)
                model = ARIMA(
                    series,
                    order=candidate_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                )
                fitted_model = model.fit()

            if candidate_order != primary_order:
                logger.warning(
                    "Primary ARIMA%s did not converge; using fallback ARIMA%s instead",
                    primary_order,
                    candidate_order,
                )

            return fitted_model
        except (ConvergenceWarning, ValueError, RuntimeError, TypeError) as error:
            last_error = error

    if last_error is not None:
        raise ValueError(f"Forecast model fitting failed: {last_error}") from last_error

    raise ValueError("Forecast model fitting failed: insufficient data for available ARIMA orders")


def forecast_temperature(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """
    Forecast future temperature using ARIMA
    """

    try:
        df = df.copy()
        date_col = config["columns"]["date"]
        temp_col = config["columns"]["temperature"]

        steps = int(config["forecast"]["steps"])
        order = tuple(config["forecast"]["arima_order"])

        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")
        df = df.dropna(subset=[date_col, temp_col])
        df = df.sort_values(by=date_col).drop_duplicates(subset=[date_col], keep="last")

        if df.empty:
            raise ValueError("No valid temperature observations are available for forecasting")

        series = df.set_index(date_col)[temp_col].asfreq("D")
        series = series.interpolate(limit_direction="both").dropna()

        min_observations = _minimum_observations(order)
        if len(series) < min_observations:
            raise ValueError(
                f"At least {min_observations} observations are required for ARIMA{order} forecasting"
            )

        # Train model
        model_fit = _fit_arima_with_fallback(series, order)

        forecast = model_fit.forecast(steps=steps)

        forecast_df = forecast.rename("forecast_temperature").reset_index()
        forecast_df.columns = [date_col, "forecast_temperature"]

        logger.info("Forecasting completed")

        return forecast_df

    except Exception as e:
        logger.error(f"Forecasting failed: {e}")
        raise


def forecast_arima(df: pd.DataFrame, steps: int = 30, arima_order: tuple = (5, 1, 0)) -> Dict:
    """
    Forecast future values using ARIMA - simplified interface for Streamlit dashboard.
    
    Args:
        df: DataFrame with single column of values to forecast
        steps: Number of steps to forecast
        arima_order: ARIMA order tuple (p, d, q)
    
    Returns:
        Dictionary with 'forecast' key containing forecast values
    """
    try:
        # Extract the single column
        series = df.iloc[:, 0].astype(float).dropna()
        
        if len(series) < _minimum_observations(arima_order):
            raise ValueError(f"Insufficient data for ARIMA{arima_order} forecasting")
        
        # Fit model
        model_fit = _fit_arima_with_fallback(series, arima_order)
        
        # Generate forecast
        forecast = model_fit.forecast(steps=steps)
        
        logger.info(f"ARIMA{arima_order} forecast completed for {steps} steps")
        
        return {
            "forecast": forecast.values.tolist(),
            "model_order": arima_order,
            "steps": steps,
        }
    
    except Exception as e:
        logger.error(f"ARIMA forecasting failed: {e}")
        raise
