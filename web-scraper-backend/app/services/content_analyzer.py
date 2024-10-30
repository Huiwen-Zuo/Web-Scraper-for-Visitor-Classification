from typing import Dict, List, Set
from collections import defaultdict
import logging
import re

logger = logging.getLogger(__name__)

class ContentAnalyzer:
    def __init__(self):
        self.content_categories = {
            'technical': {
                'keywords': {'api', 'code', 'documentation', 'implementation', 'developer', 'sdk', 'library', 'framework', 'integration'},
                'weight': 1.2
            },
            'business': {
                'keywords': {'pricing', 'enterprise', 'solution', 'roi', 'cost', 'business', 'service', 'partnership'},
                'weight': 1.1
            },
            'educational': {
                'keywords': {'learn', 'guide', 'tutorial', 'course', 'example', 'getting started', 'basics'},
                'weight': 1.0
            },
            'support': {
                'keywords': {'help', 'contact', 'support', 'assistance', 'troubleshooting', 'faq'},
                'weight': 0.9
            }
        }

    def categorize_content(self, content: Dict) -> Dict[str, Dict]:
        """
        Categorize content sections and their relevance
        """
        category_scores = defaultdict(lambda: {'score': 0.0, 'sections': []})
        
        # Analyze each content section
        for section_type, texts in content.items():
            if not isinstance(texts, list):
                texts = [texts]
            
            for text in texts:
                if not text:
                    continue
                    
                text_lower = text.lower()
                
                # Score each category
                for category, info in self.content_categories.items():
                    score = self._calculate_category_score(text_lower, info['keywords'])
                    if score > 0:
                        weighted_score = score * info['weight']
                        category_scores[category]['score'] += weighted_score
                        category_scores[category]['sections'].append({
                            'text': text,
                            'type': section_type,
                            'relevance': weighted_score
                        })
        
        return dict(category_scores)

    def _calculate_category_score(self, text: str, keywords: Set[str]) -> float:
        """
        Calculate how relevant a text is to a category based on keyword matches
        """
        score = 0.0
        text_words = set(re.findall(r'\w+', text.lower()))
        
        for keyword in keywords:
            if ' ' in keyword:  # Multi-word keyword
                if keyword in text.lower():
                    score += 2.0  # Higher weight for phrase matches
            elif keyword in text_words:
                score += 1.0
                
        return score / len(text_words) if text_words else 0.0


class UserProfiler:
    def __init__(self):
        self.intent_patterns = {
            'developer': {
                'indicators': {
                    'technical details': 2.0,
                    'api': 1.5,
                    'implementation': 1.5,
                    'documentation': 1.2,
                    'code': 1.2
                },
                'content_priority': ['documentation', 'api_reference', 'code_samples', 'technical_guides']
            },
            'business_decision_maker': {
                'indicators': {
                    'pricing': 2.0,
                    'enterprise': 1.5,
                    'solution': 1.5,
                    'roi': 1.8,
                    'cost': 1.2
                },
                'content_priority': ['pricing', 'case_studies', 'enterprise_solutions', 'contact_sales']
            },
            'learner': {
                'indicators': {
                    'tutorial': 2.0,
                    'learn': 1.5,
                    'guide': 1.5,
                    'example': 1.2,
                    'basics': 1.2
                },
                'content_priority': ['tutorials', 'getting_started', 'examples', 'learning_paths']
            }
        }

    def analyze_intent(self, answers: Dict[str, str], content_categories: Dict) -> Dict:
        """
        Analyze user intent based on their answers and content categories
        """
        intent_scores = defaultdict(float)
        confidence_factors = []

        # Analyze answers
        for question_id, answer in answers.items():
            answer_lower = answer.lower()
            
            # Score each intent based on answer patterns
            for intent, pattern in self.intent_patterns.items():
                for indicator, weight in pattern['indicators'].items():
                    if indicator in answer_lower:
                        intent_scores[intent] += weight
                        confidence_factors.append(weight)

        # Consider content categories in intent analysis
        for category, data in content_categories.items():
            category_score = data['score']
            if category == 'technical':
                intent_scores['developer'] += category_score * 0.5
            elif category == 'business':
                intent_scores['business_decision_maker'] += category_score * 0.5
            elif category == 'educational':
                intent_scores['learner'] += category_score * 0.5

        # Calculate primary intent and confidence
        if intent_scores:
            primary_intent = max(intent_scores.items(), key=lambda x: x[1])
            total_score = sum(intent_scores.values())
            confidence = primary_intent[1] / total_score if total_score > 0 else 0.0
        else:
            primary_intent = ('unknown', 0.0)
            confidence = 0.0

        return {
            'primary_intent': primary_intent[0],
            'confidence': confidence,
            'intent_scores': dict(intent_scores),
            'content_priorities': self.intent_patterns[primary_intent[0]]['content_priority']
        }