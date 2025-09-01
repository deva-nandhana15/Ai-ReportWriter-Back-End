import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
COLAB_API_URL = os.getenv("COLAB_API_URL", "https://abcd-1234.ngrok.io")  # Replace with your ngrok URL

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET")
