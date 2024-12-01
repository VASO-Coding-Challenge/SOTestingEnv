from dotenv import load_dotenv
import os

__authors__ = ["Mustafa Aljumayli"]

load_dotenv(os.path.join(os.getcwd(), "backend/.env.development"))

# Access the environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = os.getenv("ALGORITHM")
