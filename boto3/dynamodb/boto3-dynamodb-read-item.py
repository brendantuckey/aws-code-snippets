"""
Gets an item from the dynamodb table named Movies

Technologies: python, boto3

Related Boto3 Documentation:
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

To run in Cloud 9 environment:
    python3 filename
OR
    Run button from code editor

Author: Brendan Tuckey
File location: https://github.com/brendantuckey/aws-code-snippets/blob/latest/boto3/dynamodb
Updated: 3/24/2024
"""

#!/usr/bin/python3
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

def get_movie(title, year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Movies')
    try:
        response = table.get_item(Key={'year': year, 'title': title})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


if __name__ == '__main__':
    movie = get_movie("The Big New Movie", 2015)
    if movie:
        print("Get movie succeeded:")
        pprint(movie, sort_dicts=False)
