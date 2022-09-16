import datetime
from urllib import response
from venv import create
from .models import Question
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

class QuestionModelTest(TestCase):

    def test_future_publish_recent(self):
        time = timezone.now() + datetime.timedelta(days=30)
        furure_question = Question(pub_date=time)
        self.assertIs(furure_question.was_publish_recently(), False)
    
    def test_old_publish_recent(self):
        time = timezone.now() - datetime.timedelta(days=20)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_publish_recently(), False)

    def test_recent_publish_recent(self):
        time = timezone.now()
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_publish_recently(), True)

def create_question(text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)

class QuestionIndexView(TestCase):

    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_question(self):
        question = create_question(text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'], [question],)
    
    def test_future_question(self):
        question = create_question(text="future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_n_future_question(self):
        future_question = create_question(text="future question", days=30)
        past_question = create_question(text='past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'], [past_question],)

    def test_question_order(self):
        past_question = create_question(text="past question", days=-20)
        recent_question = create_question(text="recent_question", days=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'],[recent_question, past_question])

class QuestionDetailView(TestCase):
    
    def test_future_question(self):
        future_question = create_question(text='future', days=1)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(text="past", days=-10)
        response = self.client.get(reverse('polls:detail',args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)





    



    
    
