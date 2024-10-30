import os
from dotenv import load_dotenv
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai_access():
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    logger.info(f"API Key found: {'Yes' if api_key else 'No'}")
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        logger.info("API Test successful!")
        logger.info(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        logger.error(f"API Test failed: {str(e)}")

if __name__ == "__main__":
    test_openai_access() 