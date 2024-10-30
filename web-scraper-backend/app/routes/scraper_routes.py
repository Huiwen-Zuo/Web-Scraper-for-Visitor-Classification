from flask import Blueprint, request, jsonify
from app.services.scraper_service import ScraperService
from app.services.classifier_service import ClassifierService
from app.models.schemas import UrlSchema, AnswersSchema
from app.services.aws_service import AWSService
import os
import logging

logger = logging.getLogger(__name__)

scraper_bp = Blueprint('scraper', __name__)
scraper_service = ScraperService()
classifier_service = ClassifierService()

@scraper_bp.route('/scrape', methods=['POST'])
def scrape_website():
    try:
        data = request.get_json()
        url_schema = UrlSchema()
        validated_data = url_schema.load(data)
        
        questions = scraper_service.scrape_and_generate_questions(validated_data['url'])
        return jsonify({'questions': questions}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@scraper_bp.route('/classify', methods=['POST'])
def classify_visitor():
    try:
        data = request.get_json()
        answers_schema = AnswersSchema()
        validated_data = answers_schema.load(data)
        
        classification = classifier_service.classify_visitor(
            validated_data['url'],
            validated_data['answers']
        )
        return jsonify(classification), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@scraper_bp.route('/test-aws', methods=['GET'])
def test_aws():
    try:
        # Log environment variables (DO NOT use in production!)
        logger.info("AWS Credentials Check:")
        logger.info(f"AWS_ACCESS_KEY_ID exists: {bool(os.getenv('AWS_ACCESS_KEY_ID'))}")
        logger.info(f"AWS_SECRET_ACCESS_KEY exists: {bool(os.getenv('AWS_SECRET_ACCESS_KEY'))}")
        logger.info(f"AWS_REGION: {os.getenv('AWS_REGION')}")

        aws_service = AWSService()
        test_text = "Amazon Web Services (AWS) is a comprehensive cloud platform."
        
        result = aws_service.analyze_text(test_text)
        return jsonify({
            'status': 'success',
            'message': 'AWS connection successful',
            'data': result
        }), 200
    except Exception as e:
        logger.error(f"Error in test-aws route: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500