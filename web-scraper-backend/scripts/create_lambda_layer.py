import os
import shutil
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_lambda_layer():
    try:
        # Create directories
        layer_dir = "lambda_layer"
        python_dir = os.path.join(layer_dir, "python")
        
        # Clean up existing directories
        if os.path.exists(layer_dir):
            shutil.rmtree(layer_dir)
        
        os.makedirs(python_dir)
        logger.info(f"Created layer directory: {python_dir}")
        
        # Updated requirements list
        requirements = [
            'beautifulsoup4==4.9.3',
            'requests==2.26.0',
            'boto3==1.26.137',
            'lxml==4.9.3'  # Added for better HTML parsing
        ]
        
        # Install requirements
        logger.info("Installing requirements...")
        subprocess.check_call([
            'pip', 'install',
            '-t', python_dir,
            *requirements
        ])
        
        # Create ZIP file
        logger.info("Creating layer ZIP file...")
        shutil.make_archive('lambda_layer', 'zip', layer_dir)
        
        # Clean up
        shutil.rmtree(layer_dir)
        
        print("Lambda layer created successfully!")
    except Exception as e:
        logger.error(f"Failed to create Lambda layer: {e}")
        raise

if __name__ == "__main__":
    create_lambda_layer() 