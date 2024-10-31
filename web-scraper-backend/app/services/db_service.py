import boto3
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class DBService:
    def __init__(self, is_local: bool = True):
        if is_local:
            self.dynamodb = boto3.resource('dynamodb',
                endpoint_url='http://localhost:8000',
                region_name='local',
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
        else:
            self.dynamodb = boto3.resource('dynamodb')
        
        self.sessions_table = self.dynamodb.Table('UserSessions')
        self.recommendations_table = self.dynamodb.Table('Recommendations')

    def create_session(self, url: str) -> str:
        """Create a new user session"""
        session_id = str(uuid.uuid4())
        self.sessions_table.put_item(
            Item={
                'session_id': session_id,
                'url': url,
                'created_at': datetime.utcnow().isoformat(),
                'status': 'active',
                'answers': {}
            }
        )
        return session_id

    def update_session_answers(self, session_id: str, answers: Dict) -> bool:
        """Update session with user answers"""
        try:
            self.sessions_table.update_item(
                Key={'session_id': session_id},
                UpdateExpression='SET answers = :answers',
                ExpressionAttributeValues={':answers': answers}
            )
            return True
        except Exception as e:
            print(f"Error updating session: {str(e)}")
            return False

    def save_recommendations(self, session_id: str, recommendations: List[Dict]) -> str:
        """Save generated recommendations"""
        recommendation_id = str(uuid.uuid4())
        self.recommendations_table.put_item(
            Item={
                'recommendation_id': recommendation_id,
                'session_id': session_id,
                'recommendations': recommendations,
                'created_at': datetime.utcnow().isoformat()
            }
        )
        return recommendation_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session details"""
        try:
            response = self.sessions_table.get_item(
                Key={'session_id': session_id}
            )
            return response.get('Item')
        except Exception as e:
            print(f"Error getting session: {str(e)}")
            return None

    def get_recommendations(self, recommendation_id: str) -> Optional[Dict]:
        """Get saved recommendations"""
        try:
            response = self.recommendations_table.get_item(
                Key={'recommendation_id': recommendation_id}
            )
            return response.get('Item')
        except Exception as e:
            print(f"Error getting recommendations: {str(e)}")
            return None 