"""
Overview:
Launch an EC2 Instance using boto3.
The subnet id determins the VPC, AZ etc that the EC2 is launched into

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_instances.html

To run in Cloud 9 environment:
    python3 boto3-ec2-launch-new.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/23/2024
"""

import boto3

REGION = 'us-east-1'
#Determins AZ and VPC etc.
#To make a public accessible EC2 Subnet must have auto-assign public IP enabled 
SUBNET = 'subnet-08f069333d7c66cbc'

AMI_ID = 'ami-02d7fd1c2af6eead0' #get a valid id from AMI Catalog in the console
KEYNAME = 'brendan-tuckey-internship'
SG_ID = 'sg-02b43ee5b61fe6b41'

ec2 = boto3.client('ec2', region_name=REGION)

response = ec2.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sdh',
            'Ebs': {
                'VolumeSize': 10,
            },
        },
    ],
    ImageId=AMI_ID,
    InstanceType = 't2.micro',
    KeyName=KEYNAME,
    MaxCount=1,
    MinCount=1,
    # Specify to associate a public IP address with the instance
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeviceIndex': 0,
            'SubnetId': SUBNET,
            'Groups': [SG_ID]  # Associate security group with network interface
        }
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Purpose',
                    'Value': 'test',
                },
                {
                    'Key': 'Name',
                    'Value': 'Test boto3 launch',
                },
            ],
        },
    ],
)

print(response)

instanceid = response['Instances'][0]['InstanceId']
print('InstanceId = ' + instanceid)

"""
Expected output:
{
    'ResponseMetadata': {
        '...': '...',
    },
}
InstanceId = '...'
"""
