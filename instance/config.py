import os

# Example: Overriding some configurations for local use
SECRET_KEY = "supersecretkey"  # Update this with a secure key
SQLALCHEMY_DATABASE_URI = "sqlite:///instance_app.db"
TRANSLATOR_API_KEY = "your-local-translator-key"
TRANSLATOR_REGION = "your-region"
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "instance_uploads")
