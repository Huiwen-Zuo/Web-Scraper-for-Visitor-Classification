from typing import Dict, List
import logging
from openai import OpenAI
import os
import json
from collections import Counter

logger = logging.getLogger(__name__)

class IntelligentClassifier:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.openai_client = OpenAI(api_key=api_key)

    def generate_smart_question(self, content: Dict) -> Dict:
        """
        Generate intelligent questions using GPT with fallback
        """
        try:
            logger.info("Attempting to generate question using GPT")
            return self._generate_gpt_question(content)
        except Exception as e:
            logger.error(f"GPT question generation failed: {str(e)}")
            logger.info("Falling back to rule-based analysis")
            return self._generate_fallback_question(content)

    def _generate_gpt_question(self, content: Dict) -> Dict:
        """
        Generate question using GPT
        """
        content_summary = self._prepare_content_summary(content)
        
        prompt = f"""
        Analyze this website content and generate ONE multiple-choice question to understand visitor intent.
        The question should help classify why the visitor is on this website.
        
        Website Content Summary:
        {content_summary}

        Requirements:
        1. Question should be relevant to the website's main purpose
        2. Options should be distinct and cover different intents
        3. Include 4 options (A, B, C, D)
        4. Each option should represent a different category of intent

        Return ONLY a JSON object in this format:
        {{
            "question": "the main question",
            "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
            "category_mapping": {{
                "A": "category1",
                "B": "category2",
                "C": "category3",
                "D": "category4"
            }},
            "confidence": 0.95
        }}
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing websites and understanding user intent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={ "type": "json_object" }
        )

        return json.loads(response.choices[0].message.content)

    def generate_recommendations(self, content: Dict, answers: Dict[str, str], 
                               aws_analysis: Dict) -> Dict:
        """
        Generate recommendations based on user answers and content analysis
        """
        try:
            # Prepare context for GPT
            context = {
                'content_summary': self._prepare_content_summary(content),
                'user_answers': answers,
                'aws_analysis': aws_analysis
            }
            
            prompt = f"""
            Based on the website content and user's answers, generate personalized recommendations.
            
            Website Content:
            {context['content_summary']}
            
            User Answers:
            {json.dumps(context['user_answers'], indent=2)}
            
            AWS Analysis:
            {json.dumps(context['aws_analysis'], indent=2)}
            
            Return ONLY a JSON object with recommendations in this format:
            {{
                "primary_intent": "user's main intent category",
                "recommendations": [
                    {{
                        "type": "content_section or action",
                        "title": "recommendation title",
                        "description": "brief description",
                        "priority": 1-5
                    }}
                ],
                "confidence": 0.95
            }}
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in analyzing user intent and providing recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={ "type": "json_object" }
            )

            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._generate_fallback_recommendations(content, answers)

    def _prepare_content_summary(self, content: Dict) -> str:
        """
        Prepare a concise summary of the content for GPT
        """
        summary_parts = []
        
        if content.get('title'):
            summary_parts.append(f"Title: {content['title']}")
        
        if content.get('meta_description'):
            summary_parts.append(f"Description: {content['meta_description']}")
        
        if content.get('headings'):
            summary_parts.append(f"Main Headings: {' | '.join(content['headings'][:5])}")
        
        if content.get('paragraphs'):
            # Get first paragraph and any paragraphs containing key terms
            key_paragraphs = [p for p in content['paragraphs'][:5] 
                            if any(term in p.lower() for term in ['about', 'service', 'product', 'help'])]
            if key_paragraphs:
                summary_parts.extend(key_paragraphs[:2])  # Add up to 2 key paragraphs

        return "\n".join(summary_parts)[:4000]  # Keep within GPT context limit

    def _generate_fallback_question(self, content: Dict) -> Dict:
        """
        Generate a fallback question when GPT fails
        """
        # Default general-purpose question
        default_question = {
            "question": "What information are you looking for?",
            "options": [
                "A. Product Information",
                "B. Technical Documentation",
                "C. Support/Help",
                "D. General Information"
            ],
            "category_mapping": {
                "A": "product",
                "B": "technical",
                "C": "support",
                "D": "general"
            },
            "confidence": 0.7
        }

        try:
            # Basic content analysis for better fallback
            keywords = self._extract_keywords(content)
            content_type = self._determine_content_type(keywords)
            
            # If we can determine content type, use a more specific template
            if content_type in self._get_question_templates():
                return self._get_question_templates()[content_type]
            
            return default_question
            
        except Exception as e:
            logger.error(f"Error in fallback question generation: {str(e)}")
            return default_question

    def _extract_keywords(self, content: Dict) -> Counter:
        """
        Extract and count important keywords from content
        """
        keywords = Counter()
        
        # Combine all text content
        all_text = ' '.join([
            content.get('title', ''),
            content.get('meta_description', ''),
            *content.get('headings', []),
            *content.get('paragraphs', [])[:3]  # Limit to first 3 paragraphs
        ]).lower()
        
        # Count important keywords
        for word in all_text.split():
            if word in self._get_important_keywords():
                keywords[word] += 1
                
        return keywords

    def _get_important_keywords(self) -> set:
        """
        Get set of important keywords for classification
        """
        return {
            'product', 'service', 'buy', 'price',  # Commercial
            'documentation', 'api', 'code', 'developer',  # Technical
            'help', 'support', 'contact', 'assistance',  # Support
            'about', 'company', 'team', 'mission',  # Information
            'learn', 'course', 'training', 'education'  # Educational
        }

    def _determine_content_type(self, keywords: Counter) -> str:
        """
        Determine content type based on keyword frequency
        """
        type_scores = {
            'commercial': sum(keywords[k] for k in ['product', 'service', 'buy', 'price']),
            'technical': sum(keywords[k] for k in ['documentation', 'api', 'code', 'developer']),
            'support': sum(keywords[k] for k in ['help', 'support', 'contact', 'assistance']),
            'information': sum(keywords[k] for k in ['about', 'company', 'team', 'mission']),
            'educational': sum(keywords[k] for k in ['learn', 'course', 'training', 'education'])
        }
        
        return max(type_scores.items(), key=lambda x: x[1])[0] if any(type_scores.values()) else 'general'

    def _get_question_templates(self) -> Dict:
        """
        Get question templates for different content types
        """
        return {
            'commercial': {
                "question": "What are you looking to do on this website?",
                "options": [
                    "A. Purchase Products/Services",
                    "B. Compare Prices",
                    "C. Learn About Features",
                    "D. Contact Sales"
                ],
                "category_mapping": {
                    "A": "purchase",
                    "B": "research",
                    "C": "information",
                    "D": "contact"
                },
                "confidence": 0.8
            },
            'technical': {
                "question": "What technical information are you seeking?",
                "options": [
                    "A. API Documentation",
                    "B. Implementation Guides",
                    "C. Code Examples",
                    "D. Technical Support"
                ],
                "category_mapping": {
                    "A": "api",
                    "B": "guides",
                    "C": "examples",
                    "D": "support"
                },
                "confidence": 0.8
            }
            # Add more templates as needed
        }