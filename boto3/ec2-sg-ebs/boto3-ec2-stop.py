"""
Example to stop EC2 Instances with tag Name using boto3

Technologies: python, boto3

Helpful documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/index.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/stop.html

To run in Cloud 9 environment:
    python3 boto3-ec2-stop.py
OR
    Run button from code editor

Author: Brendan Tuckey
Repo location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/23/2024
"""

#!/usr/bin/python3
import boto3
def stop_ec2_instances_by_name(tagname):
    ec2 = boto3.resource('ec2', region_name='us-east-1')

    # Get all the ec2s
    response = ec2.instances.all()

    for i in response:
        if i.tags:
            # Two ways to compare the name tag for the instance. We only need one.

            # 1. returns a boolean
            f = [tagname in x.values() for x in i.tags]

            # 2. Returns the tag list after using a lambda function
            #find_my_tag = list(filter(lambda x: tagname in x.values(), i.tags))
            #if find_my_tag:
            #    print("Stopping for " + str(find_my_tag) + "instanceId " + i.id)
            #    i.stop()

            if True in f:
                print("Stopping for instanceId " + i.id)
                i.stop()

if __name__ == "__main__":
    stop_ec2_instances_by_name("HW-P1-Instance")