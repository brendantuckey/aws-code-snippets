"""
List all buckets in a region

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_bucket_policy_status.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/s3
Updated: 3/24/2024
"""

import boto3
from botocore.exceptions import ClientError

# Create an S3 client
s3_client = boto3.client('s3')

# Get a list of all buckets
response = s3_client.list_buckets()

# Iterate through each bucket
for bucket in response['Buckets']:
    bucket_name = bucket['Name']
    
    try:
        # Get the bucket policy status
        policy_status = s3_client.get_bucket_policy_status(Bucket=bucket_name)
        
        # Check if the bucket policy allows public access
        if policy_status['PolicyStatus']['IsPublic']:
            print(f"Bucket {bucket_name} has public access")
    except ClientError as e:
        # If NoSuchBucketPolicy error occurs, bucket does not have a policy
        # Implying that no public access exists through a bucket policy
        # So 'NoSuchBucketPolicy' is a valid response implying no public access
        if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
            # Handle other errors though
            print(f"Error retrieving policy status for bucket {bucket_name}: {e}")

