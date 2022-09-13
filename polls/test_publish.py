import datetime
from .models import Question
from django.test import TestCase
from django.utils import timezone

class QuestionModelTest(TestCase):

    def test_future_publish(self):
        time = timezone.now() + datetime.timedelta(days=30)
        furure_question = Question(pub_date=time)
        self.assertIs(furure_question.was_publish_recently(), False)
 
