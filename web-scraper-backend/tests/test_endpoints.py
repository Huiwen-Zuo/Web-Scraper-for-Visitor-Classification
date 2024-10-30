import requests
import json

def test_endpoints():
    base_url = 'http://localhost:5000'
    
    # Test 1: Initial Analysis
    print("\nTesting Initial Analysis...")
    analyze_response = requests.post(
        f'{base_url}/analyze',
        json={
            'url': 'https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html'
        }
    )
    
    print(f"Status Code: {analyze_response.status_code}")
    print("Response:")
    print(json.dumps(analyze_response.json(), indent=2))

    # Test 2: Submit Answers
    print("\nTesting Submit Answers...")
    submit_response = requests.post(
        f'{base_url}/submit-answers',
        json={
            'url': 'https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html',
            'answers': {
                'question_1': 'Technical Implementation',
                'question_2': 'Building a Product',
                'question_3': 'Expert'
            }
        }
    )
    
    print(f"Status Code: {submit_response.status_code}")
    print("Response:")
    print(json.dumps(submit_response.json(), indent=2))

if __name__ == '__main__':
    test_endpoints() 