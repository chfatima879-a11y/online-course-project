from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course', 'grade')

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)

class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'description')

# Ab saare models register ho gaye hain:
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)
