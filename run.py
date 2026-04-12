from app import create_app
from flask_cors import CORS
import os
app = create_app()

CORS(app, resources={r"/api/*":{"origins":"http://localhost:4200"}})

if __name__ == "__main__":
    app.run()