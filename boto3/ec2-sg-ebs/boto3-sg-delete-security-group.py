"""
Delete a security group 

Technologies: python, boto3

Documentation
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_security_group.html

Run in Cloud 9:
    python3 boto3-create-security-group.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/25/2024
"""
#!/usr/bin/python3
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='us-east-1')

groupid = 'sg-0a44c569c9f4e055d'

# Delete security group
try:
    response = ec2.delete_security_group(GroupId=groupid)
    print('Security Group Deleted, with ID: ', groupid)
except ClientError as e:
    print(e)
