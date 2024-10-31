import json
import os
from ..services.db_service import DBService
from ..services.intelligent_classifier import IntelligentClassifier

db_service = DBService(is_local=False)  # Use actual AWS DynamoDB
classifier = IntelligentClassifier()

def create_session(event, context):
    """Create a new session"""
    try:
        body = json.loads(event['body'])
        url = body.get('url')
        
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required'})
            }
        
        session_id = db_service.create_session(url)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'session_id': session_id,
                'message': 'Session created successfully'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def generate_recommendations(event, context):
    """Generate recommendations for a session"""
    try:
        body = json.loads(event['body'])
        session_id = body.get('session_id')
        answers = body.get('answers', {})
        
        if not session_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Session ID is required'})
            }
        
        # Get session
        session = db_service.get_session(session_id)
        if not session:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Session not found'})
            }
        
        # Update session with answers
        db_service.update_session_answers(session_id, answers)
        
        # Generate recommendations
        recommendations = classifier.generate_recommendations(
            {'url': session['url']}, 
            answers
        )
        
        # Save recommendations
        rec_id = db_service.save_recommendations(session_id, recommendations)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'recommendation_id': rec_id,
                'recommendations': recommendations
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 