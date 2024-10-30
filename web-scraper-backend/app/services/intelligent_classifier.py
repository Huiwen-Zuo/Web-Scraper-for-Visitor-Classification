import logging
from typing import Dict, List
from openai import OpenAI
import os
import json

logger = logging.getLogger(__name__)

class IntelligentClassifier:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.openai_client = OpenAI(api_key=api_key)

    def generate_recommendations(self, content: Dict, answers: Dict[str, str]) -> Dict:
        """
        Generate personalized recommendations based on user answers
        """
        try:
            user_answer = next(iter(answers.values()), '').strip()
            
            # Simple prompt for GPT
            prompt = (
                f"For a website visitor interested in '{user_answer}', "
                "provide 3 recommendations as a JSON object with this exact structure:\n"
                '{"recommendations": [\n'
                '  {"title": "Title here", "description": "Description here"}\n'
                ']}'
            )

            # Get GPT response
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides recommendations in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )
            
            # Parse response
            raw_response = response.choices[0].message.content.strip()
            parsed = json.loads(raw_response)
            recommendations = parsed.get('recommendations', [])
            
            # Structure recommendations
            structured_recommendations = []
            for idx, rec in enumerate(recommendations):
                structured_rec = {
                    "title": rec.get('title', 'Recommendation'),
                    "description": rec.get('description', 'No description available'),
                    "priority": idx + 1,
                    "type": "primary_action" if idx == 0 else "resource",
                    "tags": self._generate_tags(rec)
                }
                structured_recommendations.append(structured_rec)
            
            return {
                "recommendations": structured_recommendations,
                "metadata": {
                    "confidence": 0.8,
                    "primary_intent": self._determine_intent(user_answer)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._generate_fallback_recommendations(answers)

    def _generate_tags(self, rec: Dict) -> List[str]:
        """Generate tags based on recommendation content"""
        tags = []
        content = f"{rec.get('title', '')} {rec.get('description', '')}".lower()
        
        if any(word in content for word in ['learn', 'tutorial', 'course']):
            tags.append('learning')
        if any(word in content for word in ['documentation', 'reference', 'api']):
            tags.append('documentation')
        if any(word in content for word in ['download', 'install']):
            tags.append('software')
            
        return tags if tags else ['general']

    def _determine_intent(self, answer: str) -> str:
        """Determine the primary intent from user's answer"""
        answer = answer.lower()
        if any(word in answer for word in ['learn', 'tutorial', 'course']):
            return 'learning'
        if any(word in answer for word in ['documentation', 'reference']):
            return 'technical_reference'
        return 'general_information'

    def _generate_fallback_recommendations(self, answers: Dict[str, str]) -> Dict:
        """Generate fallback recommendations when API fails"""
        user_answer = next(iter(answers.values()), '').strip()
        return {
            "recommendations": [
                {
                    "title": "Getting Started Guide",
                    "description": "Start with the beginner-friendly tutorial",
                    "priority": 1,
                    "type": "primary_action",
                    "tags": ["learning", "tutorial"]
                },
                {
                    "title": "Documentation",
                    "description": "Access comprehensive documentation",
                    "priority": 2,
                    "type": "resource",
                    "tags": ["documentation", "reference"]
                }
            ],
            "metadata": {
                "confidence": 0.8,
                "primary_intent": self._determine_intent(user_answer)
            }
        }