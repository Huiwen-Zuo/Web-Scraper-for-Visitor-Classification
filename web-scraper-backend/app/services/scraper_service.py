import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import uuid
import logging
from collections import Counter
import re

logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_and_generate_questions(self, url: str) -> List[Dict]:
        """
        Scrapes website content and generates relevant questions based on the content
        """
        try:
            # Fetch and parse content
            content = self._fetch_content(url)
            topics = self._analyze_content(content)
            
            # Generate questions based on the analyzed content
            questions = self._generate_questions(topics)
            
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

    def _analyze_content(self, content: Dict) -> List[str]:
        """
        Analyzes the content to identify main topics and themes
        """
        # Combine all text content
        all_text = ' '.join([
            content['title'],
            content['meta_description'],
            *content['headings'],
            *content['paragraphs']
        ]).lower()

        # Remove common words and special characters
        common_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'}
        words = re.findall(r'\w+', all_text)
        meaningful_words = [word for word in words if word not in common_words and len(word) > 3]

        # Get most common topics
        word_freq = Counter(meaningful_words)
        return [word for word, _ in word_freq.most_common(5)]

    def _generate_questions(self, topics: List[str]) -> List[Dict]:
        """
        Generates questions based on identified topics
        """
        question_templates = [
            {
                'text': "How interested are you in {}?",
                'options': ['Very Interested', 'Somewhat Interested', 'Not Interested']
            },
            {
                'text': "How often do you engage with content about {}?",
                'options': ['Daily', 'Weekly', 'Monthly', 'Rarely']
            },
            {
                'text': "What's your experience level with {}?",
                'options': ['Expert', 'Intermediate', 'Beginner', 'No Experience']
            }
        ]

        questions = []
        for topic in topics[:3]:  # Limit to top 3 topics
            template = question_templates[len(questions) % len(question_templates)]
            questions.append({
                'id': str(uuid.uuid4()),
                'text': template['text'].format(topic.title()),
                'options': template['options']
            })

        # Add one general question
        questions.append({
            'id': str(uuid.uuid4()),
            'text': 'What is your primary purpose for visiting this website?',
            'options': ['Learning', 'Research', 'Business', 'Entertainment']
        })

        return questions 