"""Module: Gen AI Service"""

from loguru import logger
from config_fm import ConfigFM
from config_kb import configKB

# Define Gen AI Service Class
class genAIService:
    # --> Define Attributes
    def __init__(self):
        self.config_fm_class = ConfigFM()
        self.config_kb_class = configKB()

    # --> Define Methods
    def gen_ai_service(self, input_text, connection_id) -> str:
        """Gen AI Service to Generate Text"""
        try:
            # Retrieval Documents from KB
            context = self.config_kb_class.document_retrieval_service(input_text)
            logger.info('Documents successfully recovered!')

            # Create Prompting Template
            template = self.config_fm_class.create_prompting_template(input_text, context)
            logger.info('Template created successfully!')

            # Generate Text to User
            text_generated = self.config_fm_class.invoke_model_with_response_stream(template, connection_id)
            logger.info('Text returned and successfully generated!')

            return {'statusCode': 200, 'body': text_generated}
        except Exception as e:
            logger.warning(f'Error while executing gen ai service. Error: {str(e)}')
            return {'statusCode': 500, 'body': f'Error while executing gen ai service. Error: {str(e)}'}

# Init genAIService class
gen_ai_service_class = genAIService()
