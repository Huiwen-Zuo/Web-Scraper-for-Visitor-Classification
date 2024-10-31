import os
import shutil
import subprocess

def create_lambda_layer():
    # Create directories
    layer_dir = "lambda_layer"
    python_dir = os.path.join(layer_dir, "python")
    
    # Clean up existing directories
    if os.path.exists(layer_dir):
        shutil.rmtree(layer_dir)
    
    os.makedirs(python_dir)
    
    # Install requirements to the layer directory
    requirements = [
        'boto3',
        'openai',
        'python-dotenv'
    ]
    
    subprocess.check_call([
        'pip', 'install',
        '-t', python_dir,
        *requirements
    ])
    
    # Create ZIP file
    shutil.make_archive('lambda_layer', 'zip', layer_dir)
    
    # Clean up
    shutil.rmtree(layer_dir)
    
    print("Lambda layer created successfully!")

if __name__ == "__main__":
    create_lambda_layer() 