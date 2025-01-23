import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "defaultsecretkey")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    TRANSLATOR_API_KEY = os.environ.get("TRANSLATOR_API_KEY")
    TRANSLATOR_REGION = os.environ.get("TRANSLATOR_REGION")
    TRANSLATOR_ENDPOINT = os.environ.get("TRANSLATOR_ENDPOINT")

class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False
    ENV = "production"
