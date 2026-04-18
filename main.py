import logging
import traceback
from pathlib import Path

from src.utils import (
    create_directories,
    load_config,
    log_dataframe_info,
    normalize_config_paths,
    setup_logging,
)
from src.ingestion import load_data, save_processed_data, validate_data
from src.preprocessing import preprocess_data
from src.feature_engineering import create_rolling_features, create_time_features
from src.decomposition import decompose_time_series
from src.anomaly import detect_anomalies
from src.forecasting import forecast_temperature


def main():
    config = None
    logger = logging.getLogger("ClimatePipeline")

    try:
        # =========================
        # 1. LOAD CONFIG + SETUP
        # =========================
        config = normalize_config_paths(load_config())
        create_directories(config)
        setup_logging(config["logging"]["log_file"])

        logger.info("========== PIPELINE STARTED ==========")

        # =========================
        # 2. DATA INGESTION
        # =========================
        logger.info("Step 1: Loading Data")
        df = load_data(config["data"]["raw_data_path"])
        log_dataframe_info(df, "Raw Data")

        logger.info("Step 2: Validating Data")
        validate_data(df, config)

        # =========================
        # 3. PREPROCESSING
        # =========================
        logger.info("Step 3: Preprocessing Data")
        df = preprocess_data(df, config)
        log_dataframe_info(df, "After Preprocessing")

        # =========================
        # 4. FEATURE ENGINEERING
        # =========================
        logger.info("Step 4: Feature Engineering")
        df = create_time_features(df, config)
        df = create_rolling_features(df, config)
        log_dataframe_info(df, "After Feature Engineering")

        # =========================
        # 5. DECOMPOSITION
        # =========================
        logger.info("Step 5: Time-Series Decomposition")

        try:
            decompose_time_series(df, config)
            logger.info("Decomposition completed")
        except Exception as e:
            logger.warning(f"Decomposition skipped due to error: {e}")

        # =========================
        # 6. ANOMALY DETECTION
        # =========================
        logger.info("Step 6: Anomaly Detection")

        try:
            df = detect_anomalies(df, config)
            logger.info("Anomaly detection completed")
        except Exception as e:
            logger.warning(f"Anomaly detection failed: {e}")

        # =========================
        # 7. FORECASTING
        # =========================
        logger.info("Step 7: Forecasting")

        try:
            forecast_df = forecast_temperature(df, config)
            forecast_output_path = Path(config["outputs"]["reports_path"]) / "forecast.csv"
            forecast_df.to_csv(forecast_output_path, index=False)
            logger.info(f"Forecast saved successfully to {forecast_output_path}")
        except Exception as e:
            logger.warning(f"Forecasting failed: {e}")
            forecast_df = None

        # =========================
        # 8. SAVE OUTPUT
        # =========================
        logger.info("Step 8: Saving Processed Data")
        save_processed_data(df, config["data"]["processed_data_path"])

        # =========================
        # 9. FINAL STATUS
        # =========================
        logger.info("========== PIPELINE COMPLETED ==========")

        print("\nPIPELINE EXECUTED SUCCESSFULLY")
        print(f"Check outputs folder for results: {config['outputs']['reports_path']}")

        if forecast_df is not None:
            print("Forecast file generated successfully")
        else:
            print("Forecast skipped")

    except Exception as e:
        logger.error("========== PIPELINE FAILED ==========")
        logger.error(str(e))
        logger.error(traceback.format_exc())

        print("\nPIPELINE FAILED")
        if isinstance(e, FileNotFoundError):
            missing_path = getattr(e, "filename", None) or (
                config["data"]["raw_data_path"] if config else "unknown input file"
            )
            print(f"Missing input file: {missing_path}")
            print("Place a CSV at that path or update config/config.yaml.")
        else:
            print(f"Reason: {e}")

        log_path = config["logging"]["log_file"] if config else "logs/app.log"
        print(f"Check {log_path} for detailed error information")


if __name__ == "__main__":
    main()
