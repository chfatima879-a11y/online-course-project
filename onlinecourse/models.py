from django.db import models
from django.utils.timezone import now
from .models import Lesson, Enrollment

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=5)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_correct_choices = self.choice_set.filter(is_correct=True)
        selected_correct = selected_ids.filter(is_correct=True)
        if all_correct_choices.count() == selected_correct.count() and all_correct_choices.count() == selected_ids.count():
            return True
        return False

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
