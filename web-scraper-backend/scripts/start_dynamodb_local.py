import subprocess
import os

def start_dynamodb_local():
    try:
        # Get the path to dynamodb-local directory
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dynamodb_dir = os.path.join(backend_dir, 'dynamodb-local')
        
        # Command to start DynamoDB Local
        cmd = 'java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb'
        
        # Start the process in the dynamodb-local directory
        process = subprocess.Popen(cmd, shell=True, cwd=dynamodb_dir)
        print("DynamoDB Local started successfully!")
        return process
    except Exception as e:
        print(f"Error starting DynamoDB Local: {str(e)}")
        return None

if __name__ == "__main__":
    process = start_dynamodb_local()
    if process:
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            print("\nDynamoDB Local stopped.") 