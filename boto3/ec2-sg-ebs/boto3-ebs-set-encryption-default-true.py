"""
Sets the EBS Volume encryption default to true so all future volumes are encrypted by default.

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_ebs_encryption_by_default.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""

import boto3

AWS_REGION = 'us-east-1'
session = boto3.Session(region_name=AWS_REGION)
ec2 = session.client('ec2')

def main():
    ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    # For all AWS Regions
    for region in ec2_regions:
        if region == AWS_REGION: # just do for our region as don't have permissions for all regions
            conn = boto3.client('ec2', region_name=region)
            print ("Checking AWS Region: " + region)
            status = conn.get_ebs_encryption_by_default()
            result = status["EbsEncryptionByDefault"]
            if result == True:
                print ("Activated, nothing to do")
            else:
                print("Not activated, activation in progress")
                conn.enable_ebs_encryption_by_default()

if __name__ == '__main__':
    main()
