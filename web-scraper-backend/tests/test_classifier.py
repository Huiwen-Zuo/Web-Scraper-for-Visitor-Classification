import os
from dotenv import load_dotenv
import sys
import logging

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.intelligent_classifier import IntelligentClassifier
from app.services.scraper_service import ScraperService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_classification():
    # Load environment variables
    load_dotenv()
    
    # Test URLs
    test_urls = [
        "https://www.python.org",
        "https://www.amazon.com",
        "https://www.github.com"
    ]
    
    scraper_service = ScraperService()
    
    for url in test_urls:
        try:
            logger.info(f"\nTesting URL: {url}")
            result = scraper_service.process_content(url)
            
            logger.info("Generated Question:")
            logger.info(f"Question: {result['question']}")
            logger.info("Options:")
            for option in result['options']:
                logger.info(f"  {option}")
            logger.info(f"Confidence: {result['metadata']['confidence']}")
            
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")

if __name__ == "__main__":
    test_classification() 