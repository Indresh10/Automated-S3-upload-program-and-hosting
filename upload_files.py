import boto3
from botocore.exceptions import ClientError
import os

s3_client = boto3.client("s3")
response = s3_client.list_buckets() # get list of buckets created by us
BUCKET_NAME = response['Buckets'][0]["Name"] # get the bucket name automatically
DIR = "./Documents" # create a folder to keep documents for uploading

try:
    for file in os.listdir(DIR): # get file names
        object_name = ""
        match file.split(".")[1]:
            case "txt":
                object_name = "e-image/textfile/" # text file directory
            case "jpg"|"png":
                object_name = "e-image/imagefile/" # image file directory
            case "doc"|"docx":
                object_name = "e-image/docfile/" # doc file directory
            case _:
                print(f"Invalid File type: {file}")
                break
        object_name+=file # create a upload path for the file
        response = s3_client.upload_file(f"{DIR}/{file}",BUCKET_NAME,object_name,ExtraArgs={'ACL': 'public-read'}) # upload file and made it publicly accesible
        print(f"File uploaded successfully to {BUCKET_NAME}")
        print(f"file:{file},uploaded_path:/{object_name}")
except ClientError as e:
    print(str(e))
