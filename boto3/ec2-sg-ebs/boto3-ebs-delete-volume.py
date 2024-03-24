"""
Deletes a volume as long as it is not attached to a volume i.e. is available.

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/1.26.85/reference/services/ec2/volume/delete.html

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
volume = ec2_resource.Volume('vol-0f1f36687e3c3772b')

if volume.state == "available":
    volume.delete()
    print(f'Volume successfully deleted')
else:
    print(f"Can't delete volume attached to EC2 instance")
    