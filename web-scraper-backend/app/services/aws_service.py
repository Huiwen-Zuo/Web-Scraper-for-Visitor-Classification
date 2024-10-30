import boto3
from typing import List, Dict
import logging
from botocore.exceptions import ClientError, BotoCoreError
import os

logger = logging.getLogger(__name__)

class AWSService:
    def __init__(self):
        try:
            self.comprehend = boto3.client('comprehend',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
            logger.info("AWS Comprehend client initialized")
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to initialize AWS client: {str(e)}")
            raise

    def analyze_text(self, text: str) -> Dict:
        """
        Analyzes text using AWS Comprehend
        """
        try:
            logger.info(f"Attempting to analyze text: {text[:100]}...")

            # Start with a simple sentiment analysis as a test
            sentiment_response = self.comprehend.detect_sentiment(
                Text=text,
                LanguageCode='en'
            )
            
            # If sentiment works, proceed with key phrases
            key_phrases_response = self.comprehend.detect_key_phrases(
                Text=text,
                LanguageCode='en'
            )

            return {
                'sentiment': sentiment_response['Sentiment'],
                'sentiment_scores': sentiment_response['SentimentScore'],
                'key_phrases': key_phrases_response['KeyPhrases']
            }

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"AWS Comprehend error: {error_code} - {error_message}")
            raise Exception(f"AWS Comprehend error: {error_code} - {error_message}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise