from django.test import TestCase
from .models import Question
from urllib import response
from django.utils import timezone
from django.urls import reverse

class Vote_test(TestCase):
    
    def test_vote_count(self):
        question = Question.objects.create(question_text="vote count", pub_date=timezone.now()-timezone.timedelta(-1))
        question.choice_set.create(choice_text="choice1", votes=0)
        select_choice = question.choice_set.all()[0]
        self.assertEqual(0, select_choice.votes, "at start votes = 0")
        select_choice.votes += 1
        self.assertEqual(1, select_choice.votes)

