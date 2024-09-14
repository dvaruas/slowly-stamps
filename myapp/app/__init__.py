import os

from app.models import db
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

# Create paths which might not exist
for path_env_var in [
    "RESOURCES_DIR",
    "USER_IMAGES_DIR",
    "STAMP_IMAGES_DIR",
]:
    if not os.path.exists(app.config.get(path_env_var)):
        os.mkdir(app.config.get(path_env_var))

with app.app_context():
    db.init_app(app=app)
    db.create_all()
    db.session.commit()

    from app.controllers import app_mod as slowly_views

    app.register_blueprint(slowly_views)
