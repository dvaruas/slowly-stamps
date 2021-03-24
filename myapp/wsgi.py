import os

from app import app


if __name__ == "__main__":
    os.environ["FLASK_ENV"] = "development"
    app.run()
