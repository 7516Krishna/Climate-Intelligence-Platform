import io
import sys
import types
import unittest
import warnings
from contextlib import redirect_stdout
from importlib import util
from pathlib import Path
from unittest import mock

import pandas as pd

import main
from src.anomaly import detect_anomalies
from src.forecasting import forecast_temperature
from src.ingestion import validate_data
from src.preprocessing import preprocess_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.csv"
FORECAST_DATA_PATH = PROJECT_ROOT / "outputs" / "reports" / "forecast.csv"
RAW_SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "climate_data.csv"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def build_config() -> dict:
    return {
        "data": {
            "raw_data_path": "data/raw/climate_data.csv",
            "processed_data_path": "data/processed/processed_data.csv",
        },
        "columns": {
            "date": "date",
            "temperature": "temperature",
            "rainfall": "rainfall",
        },
        "preprocessing": {"fill_method": "ffill"},
        "features": {"rolling_window": 3},
        "anomaly": {"contamination": 0.01},
        "forecast": {"steps": 3, "arima_order": [1, 1, 0]},
        "outputs": {
            "plots_path": "outputs/plots",
            "reports_path": "outputs/reports",
        },
        "logging": {"log_file": "logs/app.log"},
    }


class PipelineRegressionTests(unittest.TestCase):
    def test_preprocess_data_converts_numeric_and_removes_duplicate_dates(self):
        df = pd.DataFrame(
            {
                "date": ["2024-01-02", "bad-date", "2024-01-01", "2024-01-01"],
                "temperature": ["24.5", "19.0", None, "20.0"],
                "rainfall": ["1", "2", None, "0.5"],
            }
        )

        result = preprocess_data(df, build_config())

        self.assertEqual(
            result["date"].dt.strftime("%Y-%m-%d").tolist(),
            ["2024-01-01", "2024-01-02"],
        )
        self.assertEqual(result["temperature"].tolist(), [20.0, 24.5])
        self.assertEqual(result["rainfall"].tolist(), [0.5, 1.0])

    def test_preprocess_data_parses_year_values_as_year_start(self):
        df = pd.DataFrame(
            {
                "date": [2010, 2011],
                "temperature": [20.0, 21.0],
                "rainfall": [1.0, 2.0],
            }
        )

        result = preprocess_data(df, build_config())

        self.assertEqual(result["date"].dt.year.tolist(), [2010, 2011])
        self.assertEqual(result["date"].dt.month.tolist(), [1, 1])
        self.assertEqual(result["date"].dt.day.tolist(), [1, 1])

    def test_validate_data_requires_distinct_column_mappings(self):
        config = build_config()
        config["columns"]["temperature"] = "date"

        with self.assertRaisesRegex(ValueError, "three different columns"):
            validate_data(pd.DataFrame({"date": ["2024-01-01"], "rainfall": [1.0]}), config)

    def test_detect_anomalies_handles_short_series_without_crashing(self):
        df = pd.DataFrame({"temperature": [None, "21.5"]})

        result = detect_anomalies(df, build_config())

        self.assertIn("anomaly", result.columns)
        self.assertEqual(result["anomaly"].tolist(), [0, 0])

    def test_forecast_temperature_handles_duplicate_dates(self):
        dates = pd.date_range("2024-01-01", periods=10, freq="D").tolist()
        dates.append(pd.Timestamp("2024-01-05"))

        temperatures = [20, 21, 19, 22, 23, 24, 25, 24, 26, 27, 28]
        rainfall = [0.0] * len(temperatures)

        df = pd.DataFrame(
            {
                "date": [date.strftime("%Y-%m-%d") for date in dates],
                "temperature": temperatures,
                "rainfall": rainfall,
            }
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = forecast_temperature(df, build_config())

        self.assertEqual(len(result), 3)
        self.assertEqual(
            result["date"].dt.strftime("%Y-%m-%d").tolist(),
            ["2024-01-11", "2024-01-12", "2024-01-13"],
        )
        self.assertTrue(pd.api.types.is_float_dtype(result["forecast_temperature"]))

    def test_forecast_temperature_avoids_convergence_warning_on_sample_data(self):
        df = pd.read_csv(RAW_SAMPLE_DATA_PATH)

        with warnings.catch_warnings(record=True) as captured_warnings:
            warnings.simplefilter("always")
            result = forecast_temperature(df, build_config())

        warning_types = {type(item.message).__name__ for item in captured_warnings}
        self.assertNotIn("ConvergenceWarning", warning_types)
        self.assertEqual(len(result), 3)

    def test_main_reports_missing_input_file_without_unicode_crash(self):
        config = build_config()
        stdout = io.StringIO()

        missing_file_error = FileNotFoundError(
            2,
            "No such file or directory",
            "data/raw/missing.csv",
        )

        with mock.patch.object(main, "load_config", return_value=config), mock.patch.object(
            main, "create_directories"
        ), mock.patch.object(main, "setup_logging"), mock.patch.object(
            main, "load_data", side_effect=missing_file_error
        ):
            with redirect_stdout(stdout):
                main.main()

        output = stdout.getvalue()
        self.assertIn("PIPELINE FAILED", output)
        self.assertIn("Missing input file: data/raw/missing.csv", output)
        self.assertNotIn("\u274c", output)

    def test_main_runs_successfully_with_bundled_sample_data(self):
        stdout = io.StringIO()

        if PROCESSED_DATA_PATH.exists():
            PROCESSED_DATA_PATH.unlink()
        if FORECAST_DATA_PATH.exists():
            FORECAST_DATA_PATH.unlink()

        with redirect_stdout(stdout):
            main.main()

        output = stdout.getvalue()
        self.assertIn("PIPELINE EXECUTED SUCCESSFULLY", output)
        self.assertTrue(PROCESSED_DATA_PATH.exists())
        self.assertTrue(FORECAST_DATA_PATH.exists())

    def test_dashboard_button_flow_executes_cleanly(self):
        sample_csv = io.StringIO(
            "\n".join(
                [
                    "STATION,DATE,ANN-TMAX-NORMAL,ANN-PRCP-NORMAL",
                    "A,2024-01-01,20,0",
                    "A,2024-01-02,21,1",
                    "A,2024-01-03,22,0",
                    "A,2024-01-04,23,2",
                    "A,2024-01-05,24,0",
                    "A,2024-01-06,25,0",
                    "A,2024-01-07,26,0",
                    "A,2024-01-08,27,1",
                    "A,2024-01-09,28,0",
                    "A,2024-01-10,29,0",
                ]
            )
        )

        fake_streamlit = types.ModuleType("streamlit")
        fake_streamlit.set_page_config = lambda **kwargs: None
        fake_streamlit.title = lambda *args, **kwargs: None
        fake_streamlit.file_uploader = lambda *args, **kwargs: sample_csv
        fake_streamlit.subheader = lambda *args, **kwargs: None
        fake_streamlit.dataframe = lambda *args, **kwargs: None
        fake_streamlit.selectbox = (
            lambda label, options, index=0, **kwargs: options[index]
        )
        fake_streamlit.button = lambda *args, **kwargs: kwargs.get("disabled") is not True
        fake_streamlit.success = lambda *args, **kwargs: None
        fake_streamlit.line_chart = lambda *args, **kwargs: None
        fake_streamlit.error = lambda *args, **kwargs: None
        fake_streamlit.warning = lambda *args, **kwargs: None

        dashboard_path = PROJECT_ROOT / "dashboards" / "app.py"
        spec = util.spec_from_file_location("dashboard_test_module", dashboard_path)
        module = util.module_from_spec(spec)

        with mock.patch.dict(sys.modules, {"streamlit": fake_streamlit}):
            assert spec.loader is not None
            spec.loader.exec_module(module)

        self.assertTrue(hasattr(module, "validate_and_process"))


if __name__ == "__main__":
    unittest.main()
