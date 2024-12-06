"""Module: Configuration for knowledge base (KB) management"""

import os
import re
import boto3
from loguru import logger

# Define AWS Resource
agent_client = boto3.client('bedrock-agent-runtime')
bedrock_service = boto3.client('bedrock-runtime')

# Define Class for KB
class configKB:
    # --> Define Attributes 
    def __init__(self):
        self.kb_id = os.environ.get('KNOWLEDGE_BASE_ID')
        self.number_of_results ='your-number-of-results (int)'

    # --> Define Methods
    # Method: Retrieve Documents from Knowledge Base
    def retrieve_documents_from_kb(self, input_text:str) -> dict:
        """Retrieving documents from Bedrock's knowledge base"""
        # Document Retrieve
        try:
            kb_response = agent_client.retrieve(
                knowledgeBaseId=self.kb_id,
                retrievalConfiguration={
                    'vectorSearchConfiguration': {
                        'numberOfResults': self.number_of_results,
                        # 'overrideSearchType': 'HYBRID'|'SEMANTIC'
                    }
                },
                retrievalQuery={
                    'text': input_text
                }
            )
            return kb_response
        except agent_client.exceptions.ResourceNotFoundException as e:
            logger.warning(f'Resource Not Found: {str(e)}')
            return {}
        except agent_client.exceptions.AccessDeniedException as e:
            logger.warning(f'Access Denied: {str(e)}')
            return {}
        except Exception as e:
            logger.warning(f'Error while retrieving documents. Error: {str(e)}')
            return {}

    # Method: Transform recovered content
    def transform_content(self, kb_response:dict) -> str:
        """Transform recovered content"""
        try:
            # Define List with Clean Content
            clean_content_list = []
            for content in kb_response['retrievalResults']:
                # Clean Content
                clean_content = re.sub(r'\s+', ' ', content['content']['text'].replace('\r', ''))

                # Add Content
                clean_content_list.append("* " + clean_content)
                logger.info('Content successfully cleaned and concatenated')

            return '\n'.join(clean_content_list)
        except Exception as e:
            logger.warning(f'Error while transforming recovered content. Error: {str(e)}')
            return []

    # Principal Method: Document Retrieval Service
    def document_retrieval_service(self, input_text:str) -> str:
        """Document Retrieval Service using Bedrock's Knowledge Base"""
        try:
            # Retrieve Documents
            kb_response = self.retrieve_documents_from_kb(input_text)

            # Transfrom Recovered Documents
            transformed_content = self.transform_content(kb_response)

            return transformed_content
        except Exception as e:
            print(f'Error while executing document retrieval service. Error: {str(e)}')
