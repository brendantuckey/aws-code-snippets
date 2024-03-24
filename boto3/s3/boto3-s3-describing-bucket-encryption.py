"""
Lists all encryption data for  an accounts buckets

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_bucket_encryption.html

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
from botocore.exceptions import ClientError
from pprint import pprint

"""
Checks whether server-side encryption (SSE) configuration rule on
the bucket is enabled or not.
There is no option anymore to not have an encrypted bucket so it would only be for old buckets
"""
s3 = boto3.client('s3')
response = s3.list_buckets()
for bucket in response['Buckets']:
    try:
        enc = s3.get_bucket_encryption(Bucket=bucket['Name'])
        rules = enc['ServerSideEncryptionConfiguration']['Rules']
        print('Bucket: ', bucket['Name'])
        pprint('Encryption data: %s' % (rules))
        print('------------------------------------------------------')
    except ClientError as e: # if causes an exception error we knowit doesn't have SSE
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            pprint('Bucket: %s, no server-side encryption' % (bucket['Name']))
        else:
            pprint("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))

