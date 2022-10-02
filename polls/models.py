import datetime
from time import timezone
from django.db import models
from django.utils import timezone

class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published', default=timezone.now())
    end_date = models.DateTimeField('Closed date', default=timezone.now()+timezone.timedelta(7))

    def was_publish_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        return timezone.now() >= self.pub_date

    def can_vote(self):
        return self.is_published() and timezone.now() <= self.end_date

    def save(self, *args, **kwargs):
        """
        Only question that has valid published date and closed date can be saved.
        """
        if self.pub_date >= self.end_date:
            raise ValueError("Closed date should be behind published date")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_text

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.choice_text


class Votes(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)

    @property
    def question(self):
        return self.choice.question.question_text()

