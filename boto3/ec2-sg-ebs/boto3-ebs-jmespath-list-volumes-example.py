"""
List all volume ids in a region

Technologies: python, boto3, jmespath

Related Boto3 Documentation:
    No current URL... ChatGPT?

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""
import boto3
import jmespath
from pprint import pprint

AWS_REGION = "us-east-1"

ec2_client = boto3.client('ec2', region_name=AWS_REGION)
pprint(jmespath.search("Volumes[].VolumeId", ec2_client.describe_volumes()))