import os
import sys
from dotenv import load_dotenv
import unittest

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.db_service import DBService

class TestDBService(unittest.TestCase):
    def setUp(self):
        self.db_service = DBService(is_local=True)

    def test_session_workflow(self):
        # Create session
        url = "https://www.python.org"
        session_id = self.db_service.create_session(url)
        self.assertIsNotNone(session_id)

        # Update session with answers
        answers = {"question_1": "Learn Python Programming"}
        success = self.db_service.update_session_answers(session_id, answers)
        self.assertTrue(success)

        # Save recommendations
        recommendations = [
            {
                "title": "Python Tutorial",
                "description": "Basic Python tutorial",
                "priority": 1
            }
        ]
        rec_id = self.db_service.save_recommendations(session_id, recommendations)
        self.assertIsNotNone(rec_id)

        # Get session
        session = self.db_service.get_session(session_id)
        self.assertIsNotNone(session)
        self.assertEqual(session['url'], url)

        # Get recommendations
        saved_recs = self.db_service.get_recommendations(rec_id)
        self.assertIsNotNone(saved_recs)
        self.assertEqual(saved_recs['session_id'], session_id)

if __name__ == '__main__':
    load_dotenv()
    unittest.main() 