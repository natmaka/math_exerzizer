""" Constants for the app. """
import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
MY_PERSONNAL_EMAIL = os.getenv("MY_PERSONNAL_EMAIL")
MY_EMAIL = os.getenv("MY_EMAIL")


UNDERLINE = "$-----$\n"
SEPARATOR = "-------\n"
SECRET_KEY = os.getenv("SECRET_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PROBABILITE_PATH = Path("app/data_exercices/probabilite/generated")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
HASHED_ADMIN_PASSWORD = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
