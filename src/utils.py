import os
import yaml
import logging
from pathlib import Path
from typing import Any, Dict


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_path(path_value: str | Path) -> Path:
    """Resolve project-relative paths from the repository root."""
    path = Path(path_value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def load_config(config_path: str = "config/config.yaml") -> Dict:
    """Load YAML configuration file"""
    try:
        resolved_config_path = resolve_path(config_path)
        with resolved_config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load config: {e}")


def normalize_config_paths(config: Dict[str, Any]) -> Dict[str, Any]:
    """Convert configured filesystem paths into absolute project-root paths."""
    path_keys = [
        ("data", "raw_data_path"),
        ("data", "processed_data_path"),
        ("outputs", "plots_path"),
        ("outputs", "reports_path"),
        ("logging", "log_file"),
    ]

    for section, key in path_keys:
        config[section][key] = str(resolve_path(config[section][key]))

    return config


def create_directories(config: Dict) -> None:
    """Create required directories from config"""
    paths = [
        config["outputs"]["plots_path"],
        config["outputs"]["reports_path"],
        Path(config["data"]["processed_data_path"]).parent,
        Path(config["logging"]["log_file"]).parent,
    ]

    for path in paths:
        os.makedirs(path, exist_ok=True)


def setup_logging(log_file: str) -> None:
    """Setup logging configuration"""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )


def log_dataframe_info(df, name="DataFrame"):
    """Log dataframe shape and columns"""
    logging.info(f"{name} Shape: {df.shape}")
    logging.info(f"{name} Columns: {list(df.columns)}")
