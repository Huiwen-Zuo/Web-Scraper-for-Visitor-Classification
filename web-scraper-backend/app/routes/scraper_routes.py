from flask import Blueprint, request, jsonify
from ..services.scraper_service import ScraperService
import logging

logger = logging.getLogger(__name__)
scraper_bp = Blueprint('scraper', __name__)
scraper_service = ScraperService()

@scraper_bp.route('/analyze', methods=['POST'])
def analyze_url():
    try:
        data = request.get_json()
        url = data.get('url')
        previous_answers = data.get('answers')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        result = scraper_service.process_content(url, previous_answers)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in analyze_url: {str(e)}")
        return jsonify({'error': str(e)}), 500

@scraper_bp.route('/submit-answers', methods=['POST'])
def submit_answers():
    try:
        data = request.get_json()
        url = data.get('url')
        answers = data.get('answers')

        if not url or not answers:
            return jsonify({'error': 'URL and answers are required'}), 400

        result = scraper_service.process_content(url, answers)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in submit_answers: {str(e)}")
        return jsonify({'error': str(e)}), 500