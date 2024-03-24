"""
Overview:
Add a new security group to an EC2 Instance.

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_attribute.html

To run in Cloud 9 environment:
    python3 boto3-ec2-add-security-group.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/23/2024
"""


import boto3

# Initialize the EC2 client
ec2_client = boto3.client('ec2')

# Instance ID of the EC2 instance to which you want to add the security group
instance_id = 'your_instance_id'

# Security Group ID that you want to add to the instance
security_group_id = 'your_security_group_id'

# Modify the instance's security groups
response = ec2_client.modify_instance_attribute(
    InstanceId=instance_id,
    Groups=[
        security_group_id,
    ]
)

print("Security group added successfully to the instance.")