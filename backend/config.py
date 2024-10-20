from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.getcwd(), "backend/.env.development"))

# Access the environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
