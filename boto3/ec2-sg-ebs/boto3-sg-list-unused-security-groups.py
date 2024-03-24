"""
List all security groups in a region that are not associated with an ec2

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
sgs = ec2.security_groups.all()

# Create a dictionary of all security group IDs and their corresponding names
sg_id_name_map = {sg.id: sg.group_name for sg in sgs}

# Getting all instances in AWS account
instances = ec2.instances.all()

# Getting all security groups attached to instances
inssgs = set([sg['GroupId'] for ins in instances for sg in ins.security_groups])

print("The following Security groups have no associated instances (Running or stopped)")
# Removing used SGs
unused_sgs = set(sg_id_name_map.keys()) - inssgs

# Print the SG ids along with their names
count = 1
for sg_id in unused_sgs:
    sg_name = sg_id_name_map.get(sg_id, "Unknown")
    print("%2d. id: %s, Name: %s" % (count, sg_id, sg_name))
    count += 1

# Then could call delete security group code to delete the unused security groups