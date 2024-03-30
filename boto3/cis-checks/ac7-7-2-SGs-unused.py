"""
Objective: Checks which security groupd are unused.

Technologies: python, boto3

Related Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html


To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/cis-checks
Updated: 3/29/2024

"""

#!/usr/bin/python3
import sys
import boto3
import argparse
import configparser
import json
import botocore.exceptions
import traceback

ARG_HELP = """
########################## ac7-7-2-SGs-unused.py ##############################
### Audit check 7.7.3 Unused Security Groups must be removed.
###
###
### Usage:
### python ac7-7-2-SGs-unused.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name = args.region)
    all_instances = ec2.describe_instances()
    sec_groups = ec2.describe_security_groups()
    instance_sg_set = set()
    sg_set = set()
    for reservation in all_instances["Reservations"]:
        for instance in reservation["Instances"]:
            for sg in instance["SecurityGroups"]:
                instance_sg_set.add(sg["GroupName"])

    for security_group in sec_groups["SecurityGroups"]:
        sg_set.add(security_group["GroupName"])

    idle_sg = list(sg_set - instance_sg_set)
    print("List of security groups not attached to an instance. (List may include security group attached to a load balancer, etc.)")
    for sg in idle_sg:
        # Disregard the default security group
        if sg != "default":
            print(" - " + sg)



if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(description=ARG_HELP, formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        args.add_argument('--region','-r', default='us-east-1', help="AWS region name (Default: us-east-1)")
        args.add_argument('--profile','-p', dest='profile', type=str, default="default", help="Profile to use (Default: default)")
        args.add_argument('--verbose','-v', dest='verbose', action='store_true', help="Show verbose output of program")
        args = args.parse_args()
        print(ARG_HELP)
        print("Running checks on account: %s in region %s...\n\n" % (args.profile, args.region))
        # Launch Main
        main(args)
    except Exception as e:
        print("Main exception: ", e)
        traceback.print_exc()
