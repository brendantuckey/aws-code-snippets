"""
Overview:
Launch a number of EC2 Instance using boto3.
The subnet id determins the VPC, AZ etc that the EC2 is launched into

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/index.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_instances.html

To run in Cloud 9 environment:
    python3 boto3-ec2-create-instances.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ecs-sg-ebs
Updated: 3/23/2024
"""

import boto3

ec2 = boto3.resource("ec2")
count = 5
#Get these from your console. Subnet and SG must be in the same VPC
#The subnet_id determins the VPC we're using
subnet_id = 'subnet-'
sg_id = 'sg-'
key_name = 'brendan-'
ami = 'ami-048f6ed62451373d9'
itype = 't2.micro'
iname = 'HW-P1-Instance'

def create_instances(ec2, count, subnet_id, sg_id, key_name, ami, itype, iname):
    return ec2.create_instances(
        ImageId=ami,
        InstanceType=itype,
        KeyName=key_name,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeviceIndex': 0,
                'Groups':  [sg_id],
                'SubnetId': subnet_id,
            },
        ],
        TagSpecifications=[{
          'ResourceType': 'instance',
          'Tags': [{'Key': 'Name', 'Value': iname}]}],
        Monitoring={'Enabled': True},
        MinCount=count,
        MaxCount=count
        )

create_instances(ec2, count, subnet_id, sg_id, key_name, ami, itype, iname)

"""
Expected output:
Process exited with code: 0

The correct number of instances should exist in the specified subnet
"""