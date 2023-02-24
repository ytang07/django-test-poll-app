import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text: str, days: int) -> Question:
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

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

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        test appropriate text is displayed when there are no
        questions stored in the database
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
     
    def test_past_questions(self):
        """
        Questions from the past should be displayed 
        on the index page
        """
        question = create_question("past question", -30)
        q2 = create_question("past question 2", -15)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [q2, question]
        )

    def test_future_questions(self):
        """
        Questions from the future should not be displayed 
        on the index page
        """
        create_question("future question", 30)
        create_question("future question 2", 15)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )
    
    def test_future_and_past_question(self):
        """
        Question from the future should not be displayed 
        on the index page, but question from the past should
        """
        question = create_question("future question", -30)
        create_question("future question 2", 15)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in
        the future should 404
        """
        future_question = create_question("future question", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in
        the past should return the question
        """
        past_question = create_question("past question", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)