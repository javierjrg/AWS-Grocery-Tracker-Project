import os
import glob
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# AWS S3 bucket name and upload folder path
BUCKET_NAME = 'aws-grocery-tracker-uploads-project03-01'
UPLOAD_FOLDER = 'AWS-Grocery-Tracker-Project/1.0.0/'
RAW_IMAGES_PATH = '/home/ggc/greengrassv2/data/raw_images/cache/'  # Directory containing images to upload

# Initialize S3 client
s3_client = boto3.client('s3')

def upload_files():
    """Upload all files from the raw_images directory to the designated S3 bucket."""
    # Check if directory exists
    if not os.path.isdir(RAW_IMAGES_PATH):
        print(f"Directory {RAW_IMAGES_PATH} does not exist, cannot upload files.")
        return

    # Find all files in the RAW_IMAGES_PATH
    files_to_upload = glob.glob(f"{RAW_IMAGES_PATH}*")

    if not files_to_upload:
        print(f"No files found in {RAW_IMAGES_PATH} to upload.")
        return

    for file_path in files_to_upload:
        try:
            file_name = os.path.basename(file_path)  # Get only the file name
            s3_path = os.path.join(UPLOAD_FOLDER, file_name)  # Full path in S3

            # Upload file to S3
            s3_client.upload_file(file_path, BUCKET_NAME, s3_path)
            print(f"File {file_name} successfully uploaded to s3://{BUCKET_NAME}/{s3_path}")

        except (BotoCoreError, ClientError) as error:
            print(f"Failed to upload {file_name}: {error}")

if __name__ == "__main__":
    upload_files()

