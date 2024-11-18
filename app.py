from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3

app = Flask(__name__)

# Database configurations
DBHOST = os.environ.get("DBHOST") or "mysql"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT", 3306))

# S3 configurations
S3_BUCKET = os.environ.get("S3_BUCKET")  # Name of the S3 bucket
S3_IMAGE_KEY = os.environ.get("S3_IMAGE_KEY")  # Image key in the bucket
LOCAL_IMAGE_PATH = "static/background.jpg"  # Local path to store the image

# Establish a connection to MySQL
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

# Download image from S3
def download_image_from_s3():
    if not S3_BUCKET or not S3_IMAGE_KEY:
        print("S3_BUCKET or S3_IMAGE_KEY is not set. Skipping image download.")
        return

    # Explicitly set the region (replace with your actual region)
    s3 = boto3.client('s3', region_name='us-east-1')  # Example: use the correct region

    try:
        # Download the image from S3 and store it locally
        s3.download_file(S3_BUCKET, S3_IMAGE_KEY, LOCAL_IMAGE_PATH)
        print(f"Image downloaded from S3: {S3_BUCKET}/{S3_IMAGE_KEY}")
    except Exception as e:
        print(f"Error downloading image from S3: {e}")

# Fetch the image at startup
download_image_from_s3()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', background_image=LOCAL_IMAGE_PATH)

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', background_image=LOCAL_IMAGE_PATH)

# Ensure Flask is running continuously
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
