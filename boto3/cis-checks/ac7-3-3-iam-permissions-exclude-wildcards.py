"""
Objective: Dumps information on Policies that have '*' for both actions and resources

Technologies: python, boto3

Related Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html

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
################ ac7-3-3-iam-permissions-exclude-wildcards.py ##################
### Audit check 7.3.3 - All IAM permission assignments must be well defined and must not
### include wildcards. Least privilege must be applied based on role or service functions
###
### Usage:
### python ac7-3-3-iam-permissions-exclude-wildcards.py --profile <acct profile name> --region <AWS region name>
###
###############################################################################
"""

def main(args):
    iam = boto3.client("iam")
    policies = iam.list_policies(Scope='Local')['Policies']
    print("Checkng for wildcards in policy documents (Scoped to customer managed policies)...")
    #print(policies)
    #sys.exit()
    for policy in policies:
        wildcard_found = False
        policy_name = policy['PolicyName']
        #policy_id = policy['PolicyId']
        policy_arn = policy['Arn']
        
        # Get the policy version
        policy_versions_response = iam.list_policy_versions(PolicyArn=policy_arn)
        
        # Loop through policy versions to find the default version
        for version in policy_versions_response['Versions']:
            if version['IsDefaultVersion']:
                version_id = version['VersionId']
                break
        
        # Get the policy document for the default version
        policy_doc_response = iam.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)
        policy_doc = policy_doc_response['PolicyVersion']['Document']
        
        statement = policy_doc['Statement']
        #For single statement, enclose into a list for consistency
        if not isinstance(statement, list):
            statement = [statement]

        for s in statement:
            # Check if key 'NotAction' exist and omit
            if 'NotAction' in s:
                continue
            else:
                # check to see if wildcards are used for both "action" and "resource"
                action = s['Action']
                resource = s['Resource']
                if action == "*" and resource == "*":
                    # Print out policy if wildard found in the values
                    print("Wildcard used in both Action and Resource values for policy named %s:" % policy_name)
                    print(json.dumps(s, indent=4))
                    wildcard_found = True

        if not wildcard_found:
            print("Did not find policies that allow Actions: '*' on Resources:'*' for policy %s" % policy_name)



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


