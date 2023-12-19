"""Test the verif module."""
from pathlib import Path
from app.core.constants import UNDERLINE

from app.core.models.verif import verif_exercice


def test_verif_a_valid_exercice():
    """Test if a valid exercice is not modified"""
    valid_path = Path(__file__).parent.parent / "data" / "exercice_test.txt"
    with open(valid_path, "r", encoding="utf-8") as f:
        exercice = f.read()

    corrected = verif_exercice(exercice)

    assert exercice == corrected


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


def test_verif_end_double_fail():
    """Test if the exercice end with a \n and a UNDERLINE"""
    fail_path = Path(__file__).parent.parent / "data" / "double_fail_end.txt"
    with open(fail_path, "r", encoding="utf-8") as f:
        exercice = f.read()

    corrected = verif_exercice(exercice)

    assert corrected.split("\n")[-1] == ""
    assert corrected.split("\n")[-2] == UNDERLINE[:-1]
    assert corrected.split("\n")[-3] != UNDERLINE[:-1]


def test_verif_tags():
    """Test if the exercice contains <> tags"""
    fail_path = Path(__file__).parent.parent / "data" / "tags_exo.txt"
    with open(fail_path, "r", encoding="utf-8") as f:
        exercice = f.read()

    corrected = verif_exercice(exercice)

    assert "<" not in corrected
    assert ">" not in corrected
