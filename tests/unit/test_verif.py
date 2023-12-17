"""Test the verif module."""
from pathlib import Path
from app.core.constants import UNDERLINE

from app.core.models.verif import verif_exercice


def test_verif_end_fail():
    """Test if the exercice end with a \n"""
    fail_path = Path(__file__).parent.parent / "data" / "fail_end.txt"
    with open(fail_path, "r", encoding="utf-8") as f:
        exercice = f.read()

    corrected = verif_exercice(exercice)

    assert not exercice.endswith("\n")
    assert corrected.endswith("\n")


def test_verif_end_not_underline():
    """Test if the exercice end with a UNDERLINE"""
    fail_path = Path(__file__).parent.parent / "data" / "exercice_not_underline.txt"
    with open(fail_path, "r", encoding="utf-8") as f:
        exercice = f.read()

    corrected = verif_exercice(exercice)

    assert not exercice.endswith(UNDERLINE)
    assert corrected.endswith(UNDERLINE)
