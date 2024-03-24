"""
Attach a volume to an instance. Uses SSM.Client to mount the volume on to the instance also.
Note: If your account does not have permissions to use SSM on an EC2 use the manual mount version:
    boto3-ebs-attach-volume-manual-mount.py
    
Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/attach_volume.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""

import boto3

aws_region = 'us-east-1'

# ------------------------------------------------
# EC2 instance ID and volume details
# ------------------------------------------------
instance_id = 'i-00664c7f883db7632'
volume_size_gb = 10
volume_device = '/dev/xvdx'  # Change according to your instance type and configuration
mount_point = '/mnt/myvolume'  # Change as needed

# Connect to AWS
ec2 = boto3.client('ec2', region_name=aws_region)

# ------------------------------------------------
# Get the instance information to retrieve the AZ
# ------------------------------------------------
response = ec2.describe_instances(InstanceIds=[instance_id])
az = response['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']

# ------------------------------------------------
# Create a new EBS volume
# ------------------------------------------------
response = ec2.create_volume(
    AvailabilityZone=az,
    Size=volume_size_gb,
    VolumeType='gp2'  # Change volume type if needed
)
volume_id = response['VolumeId']
print("Volume ID:", volume_id)

# Wait for the volume to be available
print("Waiting for volume to be available...")
waiter = ec2.get_waiter('volume_available')
waiter.wait(VolumeIds=[volume_id])
print("Volume is now available")

# ------------------------------------------------
# Attach the volume to the instance
# ------------------------------------------------
response = ec2.attach_volume(
    Device=volume_device,
    InstanceId=instance_id,
    VolumeId=volume_id
)
print("Volume attached to instance")

# Wait for the volume to be attached
print("Waiting for volume to be attached...")
waiter = ec2.get_waiter('volume_in_use')
waiter.wait(VolumeIds=[volume_id])
print("Volume is now attached")

# ------------------------------------------------
# Mount the attached volume via SSM send command
# ------------------------------------------------

# Wait for the instance to be in a valid state for SSM commands
print("Waiting for instance to be in a valid state for SSM commands...")
waiter = ec2.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance_id])
print("Instance is now in a valid state for SSM commands")

ssm = boto3.client('ssm')

# Execute the mount command on the instance
response = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        f"sudo mkfs -t ext4 {volume_device}",
        f"sudo mkdir {mount_point}",
        f"sudo mount {volume_device} {mount_point}"
    ]}
)

command_id = response['Command']['CommandId']
print(f"Mount command sent, Command ID: {command_id}")