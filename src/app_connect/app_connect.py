"""Module: Establish Connection"""

import json

# Define Main Driver
def lambda_handler(event, context):
    """Main driver: Establish Connection"""
    _ = context

    # Establish Connection
    connection_id = event['requestContext']['connectionId']

    return {
        'statusCode': 200,
        'body': json.dumps('Connection Established')
    }
