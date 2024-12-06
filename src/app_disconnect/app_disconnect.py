"""Module: Close Connection"""

import json

# Define Main Driver
def lambda_handler(event, context):
    """Main driver: Close Connection"""
    _,_ = event, context
    return {
        'statusCode': 200,
        'body': json.dumps('Connection closed')
    }
