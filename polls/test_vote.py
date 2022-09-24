from django.test import TestCase
from .models import Question
from urllib import response
from django.utils import timezone
from django.urls import reverse

def create_question(text, start, end=30):
    start_time = timezone.now() + timezone.timedelta(start)
    end_time = timezone.now() + timezone.timedelta(end)
    return Question.objects.create(question_text=text, pub_date=start_time, end_date=end_time)

class Vote_test(TestCase):
    
    def test_vote_count(self):
        question = create_question(text="vote count", start=-30)
        question.choice_set.create(choice_text="choice1", votes=0)
        select_choice = question.choice_set.all()[0]
        self.assertEqual(0, select_choice.votes, "at start votes = 0")
        select_choice.votes += 1
        self.assertEqual(1, select_choice.votes)

    def test_future_can_vote(self):
        """
        Question which not get published and within closed date can't be voted.
        """
        question = create_question(text="future", start=36, end=366)
        self.assertIs(False, question.can_vote())

    def test_past_can_vote(self):
        """
        Question which get published and within closed date can be voted.
        """
        question = create_question(text="past", start=-36, end=1)
        self.assertIs(True, question.can_vote())

    def test_past_n_closed_can_vote(self):
        """
        Question which get published but pass closed date can't be voted. 
        """
        question = create_question(text="past", start=-36, end=-3)
        self.assertIs(False, question.can_vote())

