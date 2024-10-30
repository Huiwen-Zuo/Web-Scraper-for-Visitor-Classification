from app import create_app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    try:
        logger.info('Starting Flask server...')
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f'Failed to start server: {str(e)}') 