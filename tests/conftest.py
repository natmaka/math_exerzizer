""" fichier conftest.py """
from pathlib import Path
import pytest


@pytest.fixture
def exercice_test():
    """Return the path of the exercice_test.txt file"""
    return Path(__file__).parent / "data" / "exercice_test.txt"
