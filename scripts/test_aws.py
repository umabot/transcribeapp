import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def test_aws_connection():
    try:
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        print("Successfully connected to AWS")
        print(f"Available buckets: {[b['Name'] for b in buckets['Buckets']]}")
    except Exception as e:
        print(f"Error connecting to AWS: {e}")

if __name__ == "__main__":
    test_aws_connection()