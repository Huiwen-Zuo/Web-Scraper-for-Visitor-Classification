import boto3
from typing import List, Dict
import logging
from botocore.exceptions import ClientError
import os

logger = logging.getLogger(__name__)

class AWSService:
    def __init__(self):
        self.comprehend = boto3.client('comprehend',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

    def analyze_text(self, text: str) -> Dict:
        """
        Analyzes text using AWS Comprehend
        """
        try:
            # Get key phrases
            key_phrases_response = self.comprehend.detect_key_phrases(
                Text=text,
                LanguageCode='en'
            )

            # Get entities
            entities_response = self.comprehend.detect_entities(
                Text=text,
                LanguageCode='en'
            )

            # Get sentiment
            sentiment_response = self.comprehend.detect_sentiment(
                Text=text,
                LanguageCode='en'
            )

            return {
                'key_phrases': key_phrases_response['KeyPhrases'],
                'entities': entities_response['Entities'],
                'sentiment': sentiment_response['Sentiment'],
                'sentiment_scores': sentiment_response['SentimentScore']
            }

        except ClientError as e:
            logger.error(f"AWS Comprehend error: {str(e)}")
            raise Exception("Failed to analyze text with AWS Comprehend") 