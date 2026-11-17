from django.db import models
from django.utils.utils import timezone # Agar zaroorat ho

class Course(models.Model):
    name = models.CharField(max_length=100, default='online course')
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=100, default="lesson title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Question(models.Model):
    # Yeh raha course foreign key jo feedback mein maanga gaya hai:
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    # Yeh raha __str__ method jo feedback mein maanga gaya hai:
    def __str__(self):
        return f"Submission {self.id} for Enrollment {self.enrollment.id}"

class Enrollment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=timezone.now)
