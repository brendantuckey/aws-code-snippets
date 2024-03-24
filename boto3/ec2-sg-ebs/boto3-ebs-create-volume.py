"""
Create a volume in a region

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_volume.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""

import boto3

def create_volume(region, az, name, size=10, volumeType='gp2'):
    ec2_client = boto3.client('ec2', region_name=region)
    new_volume = ec2_client.create_volume(
        AvailabilityZone=f'{region}{az}',
        Size=size,
        VolumeType=volumeType,
        TagSpecifications=[
            {
                'ResourceType': 'volume',
                'Tags': [
                    { 'Key': 'Name',
                    'Value': name }
                ]
            }
        ]
    )
    print(f'Created volume ID: {new_volume["VolumeId"]}')


if __name__ == "__main__":
    create_volume("us-east-1", "b", "Test default volume create")