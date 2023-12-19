"""Verify if the exercice is valid"""
import logging
import re
from app.core.constants import UNDERLINE

logger = logging.getLogger(__name__)


def is_valid_exercice(exercice: str) -> bool:
    """Verify if the exercice is valid"""

    exercice_splited = exercice.split("\n")

    is_end_with_back_slash_n = exercice_splited[-1] == ""
    is_underline_at_end = exercice_splited[-2] == UNDERLINE[:-1]
    is_only_one_underline = exercice_splited[-3] != UNDERLINE[:-1]

    return is_end_with_back_slash_n and is_underline_at_end and is_only_one_underline


def verif_exercice(exercice: str) -> str:
    """Verify if the exercice is valid"""

    exercice_splited = exercice.split("\n")
    corrected_exercice = exercice

    if re.search(r"<.*?>", exercice):
        logger.warning("The exercice contains <> tags")
        corrected_exercice = re.sub(r"<.*?>", "", corrected_exercice)

    if is_valid_exercice(exercice):
        return exercice

    count_back_n_at_the_end = 0
    for text in exercice_splited[::-1]:
        if text == "":
            count_back_n_at_the_end += 1
        else:
            break

    # exercice should end with a /n
    if count_back_n_at_the_end > 1:
        logger.warning("The exercice end with a double /n")
        corrected_exercice = corrected_exercice[::-1].replace("\n", "", 1)

        return verif_exercice(corrected_exercice[::-1])

    # exercice should end with a /n
    if exercice_splited[-1] != "":
        logger.warning("The exercice does not end with a /n")
        corrected_exercice += "\n"
        return verif_exercice(corrected_exercice)

    # exercice should end with a UNDERLINE
    if exercice_splited[-2] != UNDERLINE[:-1]:
        logger.warning("The exercice does not end with a UNDERLINE")
        corrected_exercice = corrected_exercice[::-1].replace("\n", f"{UNDERLINE}\n", 1)

        return verif_exercice(corrected_exercice[::-1])

    if exercice_splited[-3] == UNDERLINE[:-1]:
        logger.warning("The exercice end with a double UNDERLINE")
        corrected_exercice = corrected_exercice[::-1].replace(UNDERLINE, "", 1)

        return verif_exercice(corrected_exercice[::-1])

    raise ValueError("This case should not happen")
