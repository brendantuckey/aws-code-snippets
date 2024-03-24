"""
Enables logging for all of your buckets and stores them in a given target bucket 

Technologies: python, boto3

Related Boto3 Documentation:
    Not sure where this information came from. Client also has methods for this.

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

s3 = boto3.resource('s3')

def setBucketPolicy(target_bucket: str):
    for bucket in s3.buckets.all():
        bucket_logging = s3.BucketLogging(bucket.name)
        if not bucket_logging.logging_enabled:
            bucket_logging.put(
                BucketLoggingStatus={
                    'LoggingEnabled': {
                    'TargetBucket': target_bucket,
                    'TargetPrefix': f'{bucket.name}/'
                    }
                }
            )
            
setBucketPolicy(target_bucket='logging-bucket-must-already-exist')