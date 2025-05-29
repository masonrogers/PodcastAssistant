import logging
import os


def setup(log_path: str | None = None) -> None:
    """Configure root logger to write to a file and the console."""
    if logging.getLogger().handlers:
        return
    if log_path is None:
        base = os.getenv("APPDATA") or os.path.expanduser("~")
        log_dir = os.path.join(base, "WhisperTranscriber")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "whisper_transcriber.log")
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(file_handler)
    root.addHandler(stream_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a logger with a NullHandler until setup() is called."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())
    return logger
