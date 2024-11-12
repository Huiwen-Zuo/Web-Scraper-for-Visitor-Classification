import os
import shutil
import zipfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_lambda_function():
    """Creates the main lambda_function.py file"""
    return '''
import json
import requests
from bs4 import BeautifulSoup
import boto3
import os

def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text()
        title = soup.title.string if soup.title else ""
        
        return {
            "title": title,
            "content": text_content[:1000]  # First 1000 chars for testing
        }
    except Exception as e:
        return {"error": str(e)}

def lambda_handler(event, context):
    try:
        url = event.get('url', '')
        
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required'})
            }
            
        result = scrape_website(url)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
'''

def create_lambda_package():
    try:
        # Get absolute paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        package_dir = os.path.join(backend_dir, "lambda_package")
        
        logger.info(f"Working directory: {backend_dir}")
        
        # Clean and create package directory
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
        os.makedirs(package_dir)
        logger.info(f"Created package directory: {package_dir}")
        
        # Create lambda_function.py
        with open(os.path.join(package_dir, 'lambda_function.py'), 'w') as f:
            f.write(create_lambda_function())
        logger.info("Created lambda_function.py")
        
        # Copy necessary directories
        directories = {
            'services': os.path.join(backend_dir, "app", "services"),
            'models': os.path.join(backend_dir, "app", "models")
        }
        
        for dir_name, src_path in directories.items():
            if os.path.exists(src_path):
                dst_path = os.path.join(package_dir, dir_name)
                shutil.copytree(src_path, dst_path)
                logger.info(f"Copied {dir_name} directory")
        
        # Create ZIP file
        zip_path = os.path.join(backend_dir, 'lambda_function.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(package_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, package_dir)
                    zipf.write(file_path, arcname)
        logger.info(f"Created ZIP file: {zip_path}")
        
        # Clean up
        shutil.rmtree(package_dir)
        logger.info("Cleaned up package directory")
        
        logger.info("Lambda package creation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error creating lambda package: {str(e)}")
        raise

if __name__ == "__main__":
    create_lambda_package() 