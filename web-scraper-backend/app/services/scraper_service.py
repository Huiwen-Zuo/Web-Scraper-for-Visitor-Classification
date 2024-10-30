import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import uuid
import logging
from collections import Counter
import re
from .aws_service import AWSService

logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self):
        self.aws_service = AWSService()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_and_generate_questions(self, url: str) -> List[Dict]:
        """
        Scrapes website content and generates relevant questions based on the content
        """
        try:
            # Fetch and parse content
            content = self._fetch_content(url)
            analysis = self._analyze_content(content)
            
            # Generate questions based on the analyzed content
            questions = self._generate_questions(analysis)
            
            return questions
            
        except Exception as e:
            logger.error(f"Error in scrape_and_generate_questions: {str(e)}")
            raise

    def _fetch_content(self, url: str) -> Dict:
        """
        Fetches and extracts relevant content from the website
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'title': soup.title.string if soup.title else '',
                'meta_description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else '',
                'headings': [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])],
                'paragraphs': [p.text.strip() for p in soup.find_all('p')],
                'links': [a.text.strip() for a in soup.find_all('a') if a.text.strip()],
            }
            
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise Exception(f"Failed to fetch website content: {str(e)}")

    def _analyze_content(self, content: Dict) -> Dict:
        """
        Analyzes the content using AWS Comprehend
        """
        # Combine relevant text
        text_to_analyze = ' '.join([
            content['title'],
            content['meta_description'],
            *content['headings'][:5],  # First 5 headings
            *content['paragraphs'][:3]  # First 3 paragraphs
        ])

        # Truncate to 5000 bytes (AWS Comprehend limit)
        text_to_analyze = text_to_analyze[:5000]

        # Get AWS analysis
        analysis = self.aws_service.analyze_text(text_to_analyze)

        # Extract key topics from analysis
        topics = []
        
        # Add entities of type ORGANIZATION, PERSON, EVENT
        for entity in analysis['entities']:
            if entity['Type'] in ['ORGANIZATION', 'PERSON', 'EVENT']:
                topics.append({
                    'text': entity['Text'],
                    'type': entity['Type'],
                    'score': entity['Score']
                })

        # Add key phrases with high scores
        for phrase in analysis['key_phrases']:
            if phrase['Score'] > 0.8:
                topics.append({
                    'text': phrase['Text'],
                    'type': 'KEY_PHRASE',
                    'score': phrase['Score']
                })

        return {
            'topics': topics,
            'sentiment': analysis['sentiment'],
            'sentiment_scores': analysis['sentiment_scores']
        }

    def _generate_questions(self, analysis: Dict) -> List[Dict]:
        """
        Generates questions based on AWS Comprehend analysis
        """
        questions = []

        # Add sentiment-based question
        sentiment = analysis['sentiment'].lower()
        questions.append({
            'id': str(uuid.uuid4()),
            'text': f"This content appears to be {sentiment}. Do you agree?",
            'options': ['Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree']
        })

        # Add topic-based questions
        for topic in analysis['topics'][:3]:  # Top 3 topics
            if topic['type'] == 'ORGANIZATION':
                questions.append({
                    'id': str(uuid.uuid4()),
                    'text': f"How familiar are you with {topic['text']}?",
                    'options': ['Very Familiar', 'Somewhat Familiar', 'Not Familiar']
                })
            elif topic['type'] == 'EVENT':
                questions.append({
                    'id': str(uuid.uuid4()),
                    'text': f"Are you interested in {topic['text']}?",
                    'options': ['Very Interested', 'Somewhat Interested', 'Not Interested']
                })
            else:
                questions.append({
                    'id': str(uuid.uuid4()),
                    'text': f"How relevant is {topic['text']} to your interests?",
                    'options': ['Very Relevant', 'Somewhat Relevant', 'Not Relevant']
                })

        return questions 