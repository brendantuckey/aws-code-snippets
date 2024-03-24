"""
Deletes a bucket that is empty
Run boto3-s3-delete-bucket-objects.py to remove objects in a non-empty bucket

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/delete_bucket.html

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

"""
Deletes an EMPTY S3 bucket in an AWS account
"""

def delete_empty_bucket(bucket_name):
    AWS_REGION = "us-east-2"
    client = boto3.client("s3", region_name=AWS_REGION)
    client.delete_bucket(Bucket=bucket_name)
    print("Amazon S3 Bucket has been deleted: ",bucket_name)

# Could work out how to pass the bucket name in or read it from a file
if __name__ == '__main__':
    delete_empty_bucket("unique-bucket-name")