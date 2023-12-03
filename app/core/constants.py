""" Constants for the app. """
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


UNDERLINE = "$-----$\n"
SEPARATOR = "-------\n"
SECRET_KEY = os.getenv("SECRET_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PROBABILITE_PATH = Path("app/data_exercices/probabilite/generated")
