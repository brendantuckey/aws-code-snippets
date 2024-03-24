"""
Example to create a security group using boto3

Technologies: python, boto3

Documentation
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_ingress.html

Run in Cloud 9:
    python3 boto3-create-security-group.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/23/2024
"""

#!/usr/bin/python3
import boto3
#from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='us-east-1')
response = ec2.describe_vpcs()["Vpcs"]

# Get a VPC Id based on it's Tag Name Value
#vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')# use this code or below code
for r in response:
    for k,v in r.items():
        if k == "Tags" and v[0]['Value'] == "DEV-VPC":
            vpc_id = r["VpcId"]

try:
    response = ec2.create_security_group(GroupName='Sec Group Name',
                                        Description='Allow http and SSH access',
                                        VpcId=vpc_id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s. ' % (security_group_id, vpc_id))

    # Note, no inbound rules created as yet so...Let's do that

    data = ec2.authorize_security_group_ingress(GroupId = security_group_id,
                                                IpPermissions=[     # A list of dictionaries
                                                    {'IpProtocol':'tcp',
                                                    'FromPort': 80,
                                                    'ToPort': 80,
                                                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                                                    {'IpProtocol':'tcp',
                                                    'FromPort': 22,
                                                    'ToPort': 22,
                                                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                                                ])

    print('Ingress Successfully set as: %s' % data)
except ClientError as e:
    print(e)

