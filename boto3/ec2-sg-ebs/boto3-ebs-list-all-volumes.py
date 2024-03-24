"""
List volumes in a region

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/1.26.86/reference/services/ec2/service-resource/volumes.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""

import boto3

AWS_REGION = "us-east-1"
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)

# volumes.all() returns a list of volumes
volume_list = ec2_resource.volumes.all()
for volume in volume_list:
    print(volume.id)
