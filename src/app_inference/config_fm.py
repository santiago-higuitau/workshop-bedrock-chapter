"""Module: Configuration for foundation model (FM) management"""

import os
import json
from loguru import logger
import boto3

# AWS resources
endpoint_url = os.environ.get('API_ENDPOINT')
ag_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
bedrock_service = boto3.client('bedrock-runtime')
agent_service = boto3.client('bedrock-agent-runtime')

# Define Class
class ConfigFM:
    #--> Attributes
    def __init__(self):
        self.anthropic_model_id = "your-anthropic-model-id" # for example. See models available on Amazon Bedrock
        self.max_tokens = 'your-max-tokens' # int
        self.temperature = 'your-temperature' # float: 0 to 1
        self.top_p = 'your-top-p' # float: 0 to 1
        self.top_k = 'your-top-k' # int

    # --> Define Methods
    # Method: Define API request to Invoke Model
    def api_request(self, input_text:str) -> dict: # Here you can define the api request according to your model
        """Define API request to invoke model"""
        return {
            "modelId": self.anthropic_model_id,
            "contentType": "application/json",
            "accept": "application/json",
            "body": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": input_text
                            }
                        ]
                    }
                ]
            }
        }

    
    # Method: Create Prompting Template
    def create_prompting_template(self, user_query:str, context:str) -> str: # This is one way
        """
        Create Prompting Template using documents retrieved from bedrock's kb

        Args:
            context: Documents retrieved from the knowledge base and formatted.
        """
        return f'''
        Instruction: your-instructions (tone and personality)

        Context: your-context (e.g.: we are a company looking for...)

        User Query:
            {user_query}

        Input Data:
            {context}

        Output: 
            your-expected-output 
            * this may include few shots, negative prompting, length of your expected output, among a number of other restrictions and indications
        '''

    # Method: Transmit Answer from Model
    def transmit_response(self, connection_id, response_chat):
        """Transmit response to chat"""
        ag_management_client.post_to_connection(
            ConnectionId=connection_id,
            Data=response_chat
        )

    # Method: Process Stream Object
    def process_stream_object(self, stream_object, connection_id):
        """Process Stream Object from fm response"""
        # Process Event
        answer = ''
        for event in stream_object:
            chunk = event.get('chunk')
            if chunk:
                try:
                    # Decode Chunk
                    decode_text = json.loads(chunk.get('bytes').decode())
                    output_text = decode_text.get('delta', {}).get('text', None)

                    # Validate Output Text
                    if output_text:
                        answer += output_text

                        # Transmit Answer
                        self.transmit_response(
                            connection_id=connection_id,
                            response_chat=answer
                        )
                except Exception as e:
                    logger.warning(f'Error while processing answer. Error: {str(e)}')
                    continue

        return answer

    # Method: Invoke FM Model from Bedrock
    def invoke_model_with_response_stream(self, input_text:str, connection_id:str):
        """Invoke LLM model from Amazon Bedrock"""
        try:
            # Define API request
            request_body = self.api_request(input_text)

            # Make requests
            fm_response = bedrock_service.invoke_model_with_response_stream(
                modelId=request_body['modelId'],
                contentType=request_body['contentType'],
                body=json.dumps(request_body['body'])
            )

            # Retrieve Stream Object
            stream_object = fm_response.get('body')
            logger.info('Stream Object Successfully recovered!')

            # Process Stream Object
            stream_answer = self.process_stream_object(stream_object, connection_id)
            logger.info(f'Streaming response successfully transmited!: {len(stream_answer)} characters')

            # Return Stream Answer
            return stream_answer
        except Exception as e:
            logger.warning(f'Error while invoke model and transmitting the response. Error: {str(e)}')
            # Transmit Answer
            self.transmit_response(
                connection_id=connection_id,
                response_chat="Por favor vuelva a enviar su solicitud!"
            )
