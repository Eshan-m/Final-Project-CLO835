from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database configurations
DBHOST = os.environ.get("DBHOST") or "mysql"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT", 3306))

# S3 configurations
MY_NAME = os.environ.get("MY_NAME", "Default Name")  # Default to 'Default Name' if not set
S3_BUCKET = os.environ.get("S3_BUCKET")  # Name of the S3 bucket
S3_IMAGE_KEY = os.environ.get("S3_IMAGE_KEY")  # Image key in the bucket
LOCAL_IMAGE_PATH = "static/background.jpg"  # Local path to store the image



# Log S3 configurations
if S3_BUCKET and S3_IMAGE_KEY:
    logging.info(f"S3 Bucket: {S3_BUCKET}, Image Key: {S3_IMAGE_KEY}")
else:
    logging.warning("S3_BUCKET or S3_IMAGE_KEY is not set. Ensure these are provided.")

# Establish a connection to MySQL
try:
    db_conn = connections.Connection(
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        password=DBPWD,
        db=DATABASE
    )
    logging.info("Database connection established successfully.")
except Exception as e:
    logging.error(f"Failed to connect to the database: {e}")

# Download image from S3
def download_image_from_s3():
    if not S3_BUCKET or not S3_IMAGE_KEY:
        logging.warning("S3_BUCKET or S3_IMAGE_KEY is not set. Skipping image download.")
        return

    # Explicitly set the region (replace with your actual region)
    s3 = boto3.client('s3', region_name='us-east-1')  # Replace with the correct region

    try:
        # Download the image from S3 and store it locally
        s3.download_file(S3_BUCKET, S3_IMAGE_KEY, LOCAL_IMAGE_PATH)
        logging.info(f"Image downloaded successfully from S3: s3://{S3_BUCKET}/{S3_IMAGE_KEY}")
    except Exception as e:
        logging.error(f"Error downloading image from S3: {e}")

# Fetch the image at startup
download_image_from_s3()

@app.route("/", methods=['GET', 'POST'])
def home():
    image_url = f"s3://{S3_BUCKET}/{S3_IMAGE_KEY}"
    logging.info(f"Background image URL used for home page: {image_url}")
    return render_template('addemp.html', background_image=LOCAL_IMAGE_PATH, MY_NAME=MY_NAME)

@app.route("/about", methods=['GET', 'POST'])
def about():
    image_url = f"s3://{S3_BUCKET}/{S3_IMAGE_KEY}"
    logging.info(f"Background image URL used for about page: {image_url}")
    return render_template('about.html', background_image=LOCAL_IMAGE_PATH)

# Ensure Flask is running continuously
if __name__ == "__main__":
    try:
        logging.info("Starting Flask application...")
        app.run(host="0.0.0.0", port=8080)
    except Exception as e:
        logging.error(f"Error running the Flask application: {e}")
