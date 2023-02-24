import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently should return False for questions
        with a pub_date in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_questions(self):
        """
        was_published_recently should return True for questions
        with a pub_date within 1 day in the past
        """
        time = timezone.now() - datetime.timedelta(hours=4)
        recent_q = Question(pub_date=time)
        self.assertIs(recent_q.was_published_recently(), True)
    
    def test_was_published_recently_with_past_questions(self):
        """
        was_published_recently should return False for questions
        with a pub_date more than 1 day in the past
        """
        time = timezone.now() - datetime.timedelta(days=3)
        recent_q = Question(pub_date=time)
        self.assertIs(recent_q.was_published_recently(), False)
