"""Loggers: warnings to stderr, warnings to file, verbose debug info to file."""

import logging
import sys

PLAIN_FORMATTER = logging.Formatter("%(levelname)s %(message)s")

TIMESTAMP_FORMATTER = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M"
)


def stderr_logger():
    """Initialize logger for printing messages, INFO and higher, to standard error."""
    stderr_info_logger = logging.getLogger("stderr_logger")
    stderr_info_logger.setLevel(logging.INFO)
    stderr_info_logger_handler = logging.StreamHandler(sys.stderr)
    stderr_info_logger_handler.setLevel(logging.INFO)
    stderr_info_logger.addHandler(stderr_info_logger_handler)
    stderr_info_logger_handler.setFormatter(PLAIN_FORMATTER)
    return stderr_info_logger


def warning_logger(output_filename="warnings.log"):
    """Logger for printing time-stamped messages, WARNING and higher, to file."""
    warningfile_logger = logging.getLogger("warningfile_logger")
    warningfile_logger.setLevel(logging.INFO)
    warningfile_logger_handler = logging.FileHandler(output_filename, mode="w")
    warningfile_logger_handler.setLevel(logging.WARNING)
    warningfile_logger.addHandler(warningfile_logger_handler)
    warningfile_logger_handler.setFormatter(TIMESTAMP_FORMATTER)
    return warningfile_logger


def debug_logger(output_filename="debug.log"):
    """Logger for printing time-stamped messages, DEBUG and higher, to file."""
    debugfile_logger = logging.getLogger("debugfile_logger")
    debugfile_logger.setLevel(logging.DEBUG)
    debugfile_logger_handler = logging.FileHandler(output_filename, mode="w")
    debugfile_logger_handler.setLevel(logging.DEBUG)
    debugfile_logger.addHandler(debugfile_logger_handler)
    debugfile_logger_handler.setFormatter(TIMESTAMP_FORMATTER)
    return debug_logger
