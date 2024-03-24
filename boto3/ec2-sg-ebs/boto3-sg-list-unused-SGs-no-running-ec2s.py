"""
List all security groups in a region that are not associated with a running instance

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

# Initialize the EC2 client
ec2_client = boto3.client('ec2', region_name='us-east-1')
ec2_resource = boto3.resource('ec2', region_name='us-east-1')

# Describe all running instances
response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# Extract instance information from the running_instances
running_instances = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        running_instances.append(instance)

# list all security groups
all_sgs = list(ec2_resource.security_groups.all())

# List SGs that are not being used
used_sgs = set([group['GroupId']
               for instance in running_instances
               for group in instance.get('SecurityGroups', [])])

unused_sgs = [sg for sg in all_sgs if sg.id not in used_sgs]

print("The following Security groups have no associated Running instances")
count = 1
for sg in unused_sgs:
    print("%2d. ID: %s  Name: %s" % (count, sg.id, sg.group_name))
    count += 1

# Then could call delete security group code to delete unused security groups