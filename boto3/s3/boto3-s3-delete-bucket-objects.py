"""
Delete all objects in a bucket.
This must be done prior to deleting a bucket

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
#!/usr/bin/python3
import boto3

"""
Deletes the ojects in an S3 bucket to get the bucket ready for deleting
"""
def delete_bucket(bucket_name):
    AWS_REGION = "us-east-2"
    #S3_BUCKET_NAME = "my-hands-on-lab-Demo"
    s3_resource = boto3.resource("s3", region_name=AWS_REGION)
    s3_bucket = s3_resource.Bucket(bucket_name)

    def cleanup_s3_bucket():
        # Deleting objects
        for s3_object in s3_bucket.objects.all():
            s3_object.delete()
        
        # Deleting objects versions if S3 versioning enabled
        for s3_object_ver in s3_bucket.object_versions.all():
            s3_object_ver.delete()
        print("S3 Bucket cleaned up")

    cleanup_s3_bucket()
    # Then we'd need to do the boto3-delete-empty-bucket.py

# Could work out how to pass the bucket name in or read it from a file
if __name__ == '__main__':
    delete_bucket("unique-bucket-name")
