import os

from config import DevConfig, ProdConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if os.environ.get("USE_DEV", "true") == "true":
    app.config.from_object(DevConfig)
else:
    app.config.from_object(ProdConfig)

# Create paths which might not exist
for path_env_var in ["RESOURCES_DIR", "USER_IMAGES_DIR", "STAMP_IMAGES_DIR"]:
    if not os.path.exists(app.config.get(path_env_var)):
        os.mkdir(app.config.get(path_env_var))

db = SQLAlchemy(app)

db.create_all()
db.session.commit()

from app.controllers import app_mod as slowly_views

app.register_blueprint(slowly_views)
