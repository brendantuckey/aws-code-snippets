"""
Example to check for running instances in a particular region

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/index.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/23/2024
"""

#!/usr/bin/python3
import boto3

region = 'us-east-1'
ec2 = boto3.resource("ec2", region)
print("The EC2 region is:", region)

# filtering out only the instances which are in running state
ec2_instance = {"Name": "instance-state-name", "Values": ["running"]}
instances = ec2.instances.filter(Filters=[ec2_instance])
for instance in instances:
    # printing results
    print("The following EC2 instance is in a running state", instance.id)

