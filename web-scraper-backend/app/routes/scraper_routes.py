from flask import Blueprint, request, jsonify
from app.services.scraper_service import ScraperService
from app.services.classifier_service import ClassifierService
from app.models.schemas import UrlSchema, AnswersSchema

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