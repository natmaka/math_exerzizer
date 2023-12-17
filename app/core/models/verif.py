"""Verify if the exercice is valid"""
import logging
from app.core.constants import UNDERLINE

logger = logging.getLogger(__name__)


def verif_exercice(exercice: str) -> str:
    """Verify if the exercice is valid"""

    corrected_exercice = exercice

    # exercice should end with a /n
    if not exercice.endswith("\n"):
        logger.warning("The exercice does not end with a /n")
        corrected_exercice += "\n"

    # exercice should end with a UNDERLINE
    if not exercice[: len("\n")].endswith(UNDERLINE):
        logger.warning("The exercice does not end with a UNDERLINE")
        corrected_exercice = corrected_exercice[::-1].replace("\n", UNDERLINE, 1)
        corrected_exercice = corrected_exercice[::-1] + "\n"

    return corrected_exercice
