import sys
import os

# Ensure the project root is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.web.app import create_app
from config.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    app = create_app()
    print(f"Starting server at http://localhost:{settings.PORT}")
    app.run(host="0.0.0.0", port=settings.PORT, debug=settings.DEBUG)
