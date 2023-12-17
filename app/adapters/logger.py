""" Module for logging"""


import logging


logging.basicConfig(
    filename="app/adapters/logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
