"""
Attach a volume to an instance. See notes at the bottom of file for mounting.

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/volume/attach_to_instance.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""

import boto3

def attach_volume(region, volumeId, instanceId, mountPath):
    ec2_resource = boto3.resource('ec2', region_name=region)


    volume = ec2_resource.Volume(volumeId)
    print(f'Volume {volume.id} status -> {volume.state}')
    volume.attach_to_instance(
        Device=mountPath,
        InstanceId=instanceId
    )
    print(f'Volume {volume.id} status -> {volume.state}')

if __name__ == "__main__":
    attach_volume("us-east-1", "vol-0f1f36687e3c3772b", "i-00664c7f883db7632", '/dev/sdx')

"""
This does not mount the volume
Need to go into your instance and:
    sudo mkfs -t ext4 /dev/sdx
    sudo mkdir /mnt/new_volume
    sudo mount /dev/sdx /mnt/new_volume

To confirm:
    df -hT
    lsblk

"""    