import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Absolute path to the backend/ folder (where this file lives)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))




