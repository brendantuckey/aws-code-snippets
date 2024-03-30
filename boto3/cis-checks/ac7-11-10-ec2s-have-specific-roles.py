"""
Objective: Checks that EC2s have unique IAM roles.

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
from datetime import datetime

ARG_HELP = """
########################## ac7-11-10-ec2s-have-specific-roles.py ##############################
### Audit check 7.11.10 EC2 instances must be assigned IAM roles that are specific to that
### instance function.
###
###
### Usage:
### python ac7-11-10-ec2s-have-specific-roles.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    ec2 = boto3.client('ec2', region_name=args.region)
    iam = boto3.client('iam', region_name=args.region)
    reservations = ec2.describe_instances(
        Filters=[{'Name' : 'instance-state-name', 
                  'Values' : ['pending', 
                              'running', 
                              'shutting-down', 
                              'stopping',
                              'stopped']}])['Reservations']
    for res in reservations:
        for r in res['Instances']:
            # Get instance name from Tags
            for kv_pair in r['Tags']:
                if kv_pair['Key'] == 'Name':
                    instance_name = kv_pair['Value']
            instance_id = r['InstanceId']
            #Check if a role is assigned to the instance
            if 'IamInstanceProfile' in r:
                instance_profile_name = r['IamInstanceProfile']['Arn'].split('/')[-1]
                profile_details = iam.get_instance_profile(InstanceProfileName=instance_profile_name)['InstanceProfile']
                roles = profile_details['Roles']
                print("Instance %s (%s) has Instance Profile %s with these role(s) attached:" % (instance_id, instance_name, instance_profile_name))
                for role in roles:
                    role_name = role['RoleName']
                    print('\t' + role_name)
            else:
                if r['State']['Name'] == 'terminated':
                    print("Instance %s (%s) is terminated" % (instance_id, instance_name))
                else:
                    print("No IAM Role assigned to EC2 instance %s (%s)." % (instance_id, instance_name))
                    
            print('-' * 80)



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
