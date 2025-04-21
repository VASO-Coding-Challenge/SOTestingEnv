from dotenv import load_dotenv
import os

__authors__ = ["Mustafa Aljumayli", "Michelle Nguyen"]

# load_dotenv(os.path.join(os.getcwd(), "backend/.env.development"))

# Get the path of the .env file relative to this config.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env.development")

# Load environment variables from the .env file
load_dotenv(ENV_PATH)

# Access the environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Debugging: Check if the variables are loaded properly
if not SECRET_KEY:
    print("Warning: SECRET_KEY is not set in the .env file.")

print(f"ACCESS_TOKEN_EXPIRE_MINUTES: {ACCESS_TOKEN_EXPIRE_MINUTES}")
