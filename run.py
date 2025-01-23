from app import create_app
import logging

# Set the logging level and format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create the application instance
app = create_app()

if __name__ == "__main__":
    logging.info("Starting the Flask application...")
    app.run()
