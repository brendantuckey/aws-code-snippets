"""
Detaches a volume from an instance.
If the volume is mounted it needs to be unmounted first. i.e.:
    sudo umount /mnt/new_volume

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/1.28.1/reference/services/ec2/volume/detach_from_instance.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/ec2-sg-ebs
Updated: 3/24/2024
"""
import boto3

def detach_volume(region, volumeId, instanceId, mountPath):

    EC2_RESOURCE = boto3.resource('ec2', region_name=region)
    EC2_CLIENT = boto3.client('ec2', region_name=region)


    volume = EC2_RESOURCE.Volume(volumeId)
    print(f'Volume {volume.id} status -> {volume.state}')
    volume.detach_from_instance(
        Device=mountPath,
        InstanceId=instanceId
    )

    # Vaiting for volume to become available
    waiter = EC2_CLIENT.get_waiter('volume_available')
    waiter.wait(
        VolumeIds=[
            volume.id,
        ]
    )
    print(f'Volume {volume.id} status -> {volume.state}')

if __name__ == "__main__":
    detach_volume("us-east-1", "vol-04dbbab9557c70975", "i-00664c7f883db7632", '/dev/sdx')

