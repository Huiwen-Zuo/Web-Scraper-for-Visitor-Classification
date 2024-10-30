from typing import Dict
import logging
from bs4 import BeautifulSoup
import requests
from .aws_service import AWSService
from .intelligent_classifier import IntelligentClassifier

logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self):
        self.aws_service = AWSService()
        self.classifier = IntelligentClassifier()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def process_content(self, url: str, previous_answers: Dict[str, str] = None) -> Dict:
        """
        Process website content and generate either questions or recommendations
        """
        try:
            # Fetch content
            content = self._fetch_content(url)
            
            if not previous_answers:
                # First visit: Generate initial question
                return self._generate_initial_question(content)
            else:
                # Subsequent visit: Process answers and generate recommendations
                return self._generate_recommendations(content, previous_answers)
                
        except Exception as e:
            logger.error(f"Error processing content: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def _fetch_content(self, url: str) -> Dict:
        """
        Fetch and parse website content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant content
            content = {
                'title': soup.title.string if soup.title else '',
                'meta_description': soup.find('meta', {'name': 'description'})['content'] 
                    if soup.find('meta', {'name': 'description'}) else '',
                'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])],
                'paragraphs': [p.get_text().strip() for p in soup.find_all('p')],
                'links': [a.get('href') for a in soup.find_all('a') if a.get('href')],
                'url': url
            }
            
            return content
            
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise Exception(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing content from {url}: {str(e)}")
            raise Exception(f"Failed to parse content: {str(e)}")

    def _generate_initial_question(self, content: Dict) -> Dict:
        """
        Generate initial question for the user
        """
        try:
            question_data = self.classifier.generate_smart_question(content)
            return {
                'status': 'success',
                'question': question_data['question'],
                'options': question_data['options'],
                'metadata': {
                    'category_mapping': question_data['category_mapping'],
                    'confidence': question_data.get('confidence', 0.8)
                }
            }
        except Exception as e:
            logger.error(f"Error generating initial question: {str(e)}")
            return {
                'status': 'error',
                'message': 'Failed to generate question'
            }

    def _generate_recommendations(self, content: Dict, previous_answers: Dict[str, str]) -> Dict:
        """
        Generate recommendations based on user's answers
        """
        try:
            # Get AWS analysis for the content
            text_for_analysis = self._prepare_text_for_analysis(content)
            aws_analysis = self.aws_service.analyze_text(text_for_analysis)
            
            # Generate recommendations using the intelligent classifier
            recommendations = self.classifier.generate_recommendations(
                content, 
                previous_answers, 
                aws_analysis
            )
            
            return {
                'status': 'success',
                'recommendations': recommendations['recommendations'],
                'metadata': {
                    'primary_intent': recommendations['primary_intent'],
                    'confidence': recommendations.get('confidence', 0.8)
                }
            }
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {
                'status': 'error',
                'message': 'Failed to generate recommendations'
            }

    def _prepare_text_for_analysis(self, content: Dict) -> str:
        """
        Prepare content text for AWS analysis
        """
        text_parts = []
        
        if content.get('title'):
            text_parts.append(content['title'])
            
        if content.get('meta_description'):
            text_parts.append(content['meta_description'])
            
        if content.get('headings'):
            text_parts.extend(content['headings'][:5])
            
        if content.get('paragraphs'):
            text_parts.extend(content['paragraphs'][:3])
            
        return ' '.join(filter(None, text_parts))[:5000]  # AWS Comprehend limit