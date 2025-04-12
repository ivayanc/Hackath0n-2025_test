import uvicorn
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the app module is in sys.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

if __name__ == "__main__":
    print("Starting FastAPI application...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 