import os


class Config:
    DEBUG = False
    RESOURCES_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "resources")
    )
    USER_IMAGES_DIR = os.path.join(RESOURCES_DIR, "users")
    STAMP_IMAGES_DIR = os.path.join(RESOURCES_DIR, "stamps")
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(RESOURCES_DIR, "data.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(16)
