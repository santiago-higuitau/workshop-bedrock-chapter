"""Module: Inference process"""

import json
from loguru import logger
from gen_ai_service import gen_ai_service_class

def lambda_handler(event, context):
    """Main Driver Inference Process"""
    _ = context

    # Define Connection
    connection_id = event['requestContext']['connectionId']
    
    # Recovery Message
    payload = json.loads(event['body'])
    logger.info(f'Datos recibidos: {payload}')

    # Generate and transmit Response
    _ = gen_ai_service_class.gen_ai_service(
            input_text=payload['data']['message'], 
            connection_id=connection_id,
        )

    return {
        'statusCode': 200
    }
