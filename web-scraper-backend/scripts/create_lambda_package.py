import os
import shutil
import zipfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_lambda_package():
    try:
        # Get absolute paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        package_dir = os.path.join(backend_dir, "lambda_package")
        
        logger.info(f"Working directory: {backend_dir}")
        logger.info(f"Creating package directory: {package_dir}")

        # Create package directory
        try:
            if os.path.exists(package_dir):
                shutil.rmtree(package_dir)
            os.makedirs(package_dir, exist_ok=True)
            logger.info("Created package directory successfully")
        except Exception as e:
            logger.error(f"Error creating package directory: {str(e)}")
            return

        # Copy files
        try:
            # Copy lambda_handlers
            handlers_src = os.path.join(backend_dir, "app", "lambda_handlers")
            handlers_dst = os.path.join(package_dir, "lambda_handlers")
            if os.path.exists(handlers_src):
                shutil.copytree(handlers_src, handlers_dst)
                logger.info("Copied lambda_handlers")

            # Copy services
            services_src = os.path.join(backend_dir, "app", "services")
            services_dst = os.path.join(package_dir, "services")
            if os.path.exists(services_src):
                shutil.copytree(services_src, services_dst)
                logger.info("Copied services")

            # Copy models
            models_src = os.path.join(backend_dir, "app", "models")
            models_dst = os.path.join(package_dir, "models")
            if os.path.exists(models_src):
                shutil.copytree(models_src, models_dst)
                logger.info("Copied models")

        except Exception as e:
            logger.error(f"Error copying files: {str(e)}")
            return

        # Create ZIP file
        try:
            zip_path = os.path.join(backend_dir, 'lambda_function.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(package_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, package_dir)
                        zipf.write(file_path, arcname)
            logger.info("Created ZIP file successfully")
        except Exception as e:
            logger.error(f"Error creating ZIP file: {str(e)}")
            return

        # Clean up
        try:
            shutil.rmtree(package_dir)
            logger.info("Cleaned up package directory")
        except Exception as e:
            logger.error(f"Error cleaning up: {str(e)}")

        logger.info("Lambda package creation completed!")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    create_lambda_package() 