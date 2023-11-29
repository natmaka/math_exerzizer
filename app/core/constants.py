""" Constants for the app. """
import os
from dotenv import load_dotenv

load_dotenv()


UNDERLINE = "-------\n"
SECRET_KEY = os.getenv("SECRET_KEY")
