""" Module for logging"""
import logging
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent / "logs.log"

logging.basicConfig(
    filename=FILE_PATH,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
