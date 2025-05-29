import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
APP_LOG = LOG_DIR / "app.log"
INSTALLER_LOG = LOG_DIR / "installer_build.log"


def setup_logging() -> None:
    """Ensure log directory exists and configure logging handlers."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            }
        },
        "handlers": {
            "app_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(APP_LOG),
                "maxBytes": 1_000_000,
                "backupCount": 3,
                "formatter": "default",
                "encoding": "utf-8",
            },
            "installer_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(INSTALLER_LOG),
                "maxBytes": 1_000_000,
                "backupCount": 3,
                "formatter": "default",
                "encoding": "utf-8",
            },
        },
        "root": {
            "handlers": ["app_file"],
            "level": "INFO",
        },
        "loggers": {
            "build_installer": {
                "handlers": ["installer_file"],
                "level": "INFO",
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Return a logger instance."""
    return logging.getLogger(name)
