"""
List all buckets in a region

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_buckets.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/s3
Updated: 3/24/2024
"""

#!/usr/bin/python3
import boto3

AWS_REGION = "us-east-1"
client = boto3.client("s3", region_name=AWS_REGION)
response = client.list_buckets()

print("Listing Amazon S3 Buckets in your account:")

for bucket in response['Buckets']:
    print(f"-- {bucket['Name']}")
