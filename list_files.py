import re
import boto3

s3_client = boto3.client("s3")
response = s3_client.list_buckets()
BUCKET_NAME = response['Buckets'][0]["Name"]


def getObjects(prefix:list)->dict:
    files = dict()
    for pre in prefix:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME,Prefix=pre)
        f = []
        for key in response["Contents"][1:]:
            f.append(key["Key"])
        files[response["Contents"][0]["Key"]] = f
    return files

def createDirectoryStructure(name:str,data:list)->str:
    ulList = f"<h3>{name}</h3>\n<ul>\n"
    for d in data:
        ulList += f"<li><a href='https://2247217-s3.s3.amazonaws.com/{d}'>{d}</a></li>\n"
    ulList += "</ul>" 
    return ulList

def writeToHtml(html_file:str,files:str):
    with open(html_file, 'r') as f:
        content = f.read()
        content = content.replace("{% files %}", files)

    with open(html_file, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME,Prefix="e-image")
    dirs = []
    for key in response["Contents"][1:]:
        if(key["Key"].endswith("/")):
            dirs.append(key["Key"])
    print(dirs)
    files = getObjects(dirs)
    html_text = ""
    for key,value in files.items():
        html_text += createDirectoryStructure(key,value) + "\n"
    writeToHtml(html_file="index.html",files=html_text)