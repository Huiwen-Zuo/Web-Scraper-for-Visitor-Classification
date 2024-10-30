import os
from dotenv import load_dotenv
import sys
import logging
from pprint import pprint

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scraper_service import ScraperService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_recommendations():
    # Load environment variables
    load_dotenv()
    
    test_cases = [
        {
            'url': 'https://www.python.org',
            'answers': {
                'question_1': 'Learn Python Programming'
            }
        },
        {
            'url': 'https://www.github.com',
            'answers': {
                'question_1': 'Browse Documentation'
            }
        }
    ]
    
    scraper_service = ScraperService()
    
    for case in test_cases:
        try:
            logger.info(f"\n{'='*50}")
            logger.info(f"Testing recommendations for: {case['url']}")
            logger.info(f"With answers: {case['answers']}")
            logger.info(f"{'='*50}")
            
            result = scraper_service.process_content(case['url'], case['answers'])
            
            if result['status'] == 'success':
                logger.info("\nGenerated Recommendations:")
                pprint(result['recommendations'])
                logger.info(f"\nMetadata:")
                pprint(result['metadata'])
            else:
                logger.error(f"Error: {result['message']}")
            
        except Exception as e:
            logger.error(f"Error processing {case['url']}: {str(e)}")

if __name__ == "__main__":
    test_recommendations() 