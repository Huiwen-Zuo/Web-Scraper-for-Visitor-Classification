import boto3
import os
from datetime import datetime

class DynamoDBManager:
    def __init__(self, is_local=True):
        if is_local:
            self.dynamodb = boto3.resource('dynamodb', 
                endpoint_url='http://localhost:8000',
                region_name='local',
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
        else:
            self.dynamodb = boto3.resource('dynamodb')

    def create_tables(self):
        # User Sessions Table
        self.dynamodb.create_table(
            TableName='UserSessions',
            KeySchema=[
                {
                    'AttributeName': 'session_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'session_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Recommendations Table
        self.dynamodb.create_table(
            TableName='Recommendations',
            KeySchema=[
                {
                    'AttributeName': 'recommendation_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'recommendation_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        print("Tables created successfully!")

if __name__ == "__main__":
    # Create tables in local DynamoDB
    db_manager = DynamoDBManager(is_local=True)
    db_manager.create_tables() 