"""
Deletes a dynamodb table named Movies

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
import boto3

def delete_table(table_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.delete()

if __name__ == '__main__':
    delete_table('Movies')
    print("Movies table deleted.")