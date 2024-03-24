"""
Overview:
---------
Follow the instructions below to test your Cloud9 Environment is set up for Boto3.

Technologies: python, boto3

Instructions:
-------------
Create a new Cloud9 environment:
    Name it
    Click 'Create'
    Wait until it is created
    Open

Temporary credentials and a python3 environment should automatically be set up:

Check by running in the terminal shell:
    cat ~/.aws/credentials
    python3 --version

Upload this file to the Cloud9 environment (File > Upload local files...)

To run in Cloud 9 environment:
    python3 boto3-env-test-cloud9.py
OR
    Run button from code editor

Typically get a boto3 not installed error, so install boto3:
    sudo python3 -m pip install boto3
    python3 -m pip show boto3

Then try running the code again:
    python3 boto3-env-test-cloud9.py

This is typically all that is needed to set up the environment.

Need more troubleshooting? Refer to documentation:
https://docs.aws.amazon.com/cloud9/latest/user-guide/sample-python.html

"""

import boto3

# List all of your s3 buckets
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
	print(bucket.name)

# List all of your volumes
AWS_REGION = "us-east-1"
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)
for volume in ec2_resource.volumes.all():
    print(volume)
