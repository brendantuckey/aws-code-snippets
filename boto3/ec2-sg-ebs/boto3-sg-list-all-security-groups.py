
"""
List all security groups in a region

Technologies: python, boto3

Related Boto3 Documentation:
    Unable to find related documentation... ChatGPT?

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""

import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

# Fetching all security groups in AWS account
sgs = list(ec2.security_groups.all())

count = 1
for sg in sgs:
    print("%2d. id: %s  Name: %s" % (count, sg.id, sg.group_name))
    count += 1