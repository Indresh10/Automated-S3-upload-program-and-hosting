import boto3

s3_client = boto3.client("s3")
response = s3_client.list_buckets()
BUCKET_NAME = response['Buckets'][0]["Name"]
response = s3_client.list_objects_v2(Bucket=BUCKET_NAME,Prefix="e-image/textfile/")
for key in response["Contents"]:
    print(key["Key"])