"""
Creates a bucket in a given region or us-east-1 by default

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/create_bucket.html

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

def create_bucket(bucket_name):
    AWS_REGION = "us-east-1" 
    client = boto3.client("s3", region_name=AWS_REGION)

    # us-east-1 is not an accepted value for LocationConstraint
    # so if using us-east-1 (the default bucket creation location btw) you must leave out
    #location = {'LocationConstraint': AWS_REGION}
    
    response = client.create_bucket(Bucket=bucket_name)#, CreateBucketConfiguration=location)
    print("Amazon S3 bucket has been created", bucket_name)
    print(response)

# Could work out how to pass the bucket name in or read it from a file
if __name__ == '__main__':
    create_bucket("unique-bucket-name")


