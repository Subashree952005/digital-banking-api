import os
from dotenv import load_dotenv

load_dotenv(".env.docker")

BANKING_SERVICE_URL = os.getenv("BANKING_SERVICE_URL", "http://api:8000")
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", 9000))