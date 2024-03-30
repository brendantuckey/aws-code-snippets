"""
Objective: Color codes AMIs that are unencrypted.

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
########################## ac7-11-11-amis-encrypted.py ##############################
### Audit check 7.11.11 All AMIs must be encrypted at rest.
###
###
### Usage:
### python ac7-11-11-amis-encrypted.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

# ANSI escape codes for coloring output
RED = '\033[91m'
RESET = '\033[0m'

def main(args):
    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=args.region)
    
    # Describe all images
    images = ec2.describe_images(Owners=['self'])['Images']
    print("Images:")
    for image in images:
        if 'BlockDeviceMappings' in image:
            encrypted = False
            for mapping in image['BlockDeviceMappings']:
                if 'Ebs' in mapping and 'Encrypted' in mapping['Ebs'] and not mapping['Ebs']['Encrypted']:
                    encrypted = True
                    break
            if encrypted:
                print(RED + str(image) + RESET)
            else:
                print(image)
    
    # Initialize counters
    total_amis = len(images)
    unencrypted_amis = sum(1 for image in images if any('Ebs' in mapping and 'Encrypted' in mapping['Ebs'] and not mapping['Ebs']['Encrypted'] for mapping in image.get('BlockDeviceMappings', [])))
    
    # Print the counts
    print()
    print("Counts")
    print("------")
    print("Total AMIs: ", total_amis)
    print("Unencrypted AMIs: ", unencrypted_amis)


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
