
"""
Objective: Use VPC Flow log data to determine
traffic flow on what IP addresses and ports are required
to build out proper Network Access Control Lists

Technologies: python, boto3

Related Boto3 Documentation:


To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/vpc
Updated: 3/29/2024

Prerequisites:
A Default VPC with the name tag "Default" should be associated with your account
"""

#!/usr/bin/python
import boto3

#---------------------------------------------------------
# Open and read the vpcflow.log file and standardize the data
#---------------------------------------------------------
f = open('vpcflow.log', 'r')
logs = f.readlines()
f.close()
# Get headers row
headers_row = logs[0]
fields = headers_row.split()

# Build out dictionary to reference logs
logs_dictionaries = []
for l in logs[1:]:
    record = {}
    line = l.split()
    col_count = 0
    for field in fields:
        record[field] = line[col_count]
        col_count = col_count + 1
    logs_dictionaries.append(record)

# Instantiate two sets of dictionaries for inbound and outbound rule sets
inbound_rules_dict = {}
outbound_rules_dict = {}

# Start looping thru each log line
for log_line in logs_dictionaries:
    # Only look for accepted traffic
    if log_line['action'] == 'ACCEPT':
        
        if log_line['srcaddr'].startswith('10.') and int(log_line['srcport']) < 1023:
            # Create outbound ACL, traffic flowing out of our VPC
            # Use srcaddr, dstaddr, and srcport value to create a unique key for dictionary
            # Store these rules in the outbound_rules_dict dictionary
            rule = (log_line['srcaddr'], log_line['dstaddr'], log_line['srcport'], log_line['dstport'], log_line['protocol'])
            key_name = "{}_{}_{}".format(log_line['srcaddr'], log_line['dstaddr'], log_line['srcport'])
            outbound_rules_dict[key_name] = rule

        if log_line['dstaddr'].startswith('10.') and int(log_line['dstport']) <1023:
            # Create inbound ACL, traffic flowing into our VPC
            # Use srcaddr, dstaddr, and dstport value to create a unique key for dictionary
            # Store these rules in the inbound_rules_dict dictionary
            rule = (log_line['srcaddr'], log_line['dstaddr'], log_line['srcport'], log_line['dstport'], log_line['protocol'])
            key_name = "{}_{}_{}".format(log_line['srcaddr'], log_line['dstaddr'], log_line['dstport'])
            inbound_rules_dict[key_name] = rule

# Now the data should be standardized...
            
#---------------------------------------------------------
# Create a NACL
#---------------------------------------------------------

# Get the default VPC ID
region = 'us-east-1'
ec2 = boto3.resource('ec2', region_name=region)
client = boto3.client('ec2', region_name=region)
filters = [{'Name':'tag:Name', 'Values':['Default']}]

#Should return only the Default VPC ID
vpcs = list(ec2.vpcs.filter(Filters=filters))
vpc_id = vpcs[0].id

# Build out NACLs
response = client.create_network_acl(VpcId=vpc_id)
nacl_id = response['NetworkAcl']['NetworkAclId']

# Loop thru the inbound rules dictionary to define NACL entries
# Create INBOUND entries
rule_number = 100 # start rule numbering at 100 and increment by 10 for each new rule
for rule in inbound_rules_dict.values():
    # rule tuple === (src address, dst address, src port, dst port, protocol)
    response = client.create_network_acl_entry(
        CidrBlock='{}/32'.format(rule[0]),
        Egress=False,
        NetworkAclId=nacl_id,
        PortRange={
            'From': int(rule[3]),
            'To': int(rule[3]),
        },
        Protocol=rule[-1],
        RuleAction='allow',
        RuleNumber=rule_number
    )
    print(f"Inbound rule {rule_number}: Allow {rule[3]} for {rule[0]} -- {response}")
    rule_number = rule_number + 10
    

# Loop thru the outbound rules dictionary to define NACL entries
# Create OUTBOUND entries
rule_number = 100 # start rule numbering at 100 and increment by 10 for each new rule
for rule in outbound_rules_dict.values():
    # rule tuple === (src address, dst address, src port, dst port, protocol)
    response = client.create_network_acl_entry(
        CidrBlock='{}/32'.format(rule[0]),
        Egress=True,
        NetworkAclId=nacl_id,
        PortRange={
            'From': int(rule[2]),
            'To': int(rule[2]),
        },
        Protocol=rule[-1],
        RuleAction='allow',
        RuleNumber=rule_number
    )
    print(f"Outbound rule {rule_number}: Allow {rule[2]} for {rule[0]} -- {response}")
    rule_number = rule_number + 10
    