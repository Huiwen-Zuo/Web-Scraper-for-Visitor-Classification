import os
from dotenv import load_dotenv
import sys
import logging
from openai import OpenAI
from pprint import pprint

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai_models():
    # Load environment variables
    load_dotenv()
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # List available models
        models = client.models.list()
        
        logger.info("Available Models:")
        for model in models.data:
            logger.info(f"- {model.id}")
            
    except Exception as e:
        logger.error(f"Error accessing OpenAI API: {str(e)}")

if __name__ == "__main__":
    test_openai_models() 