from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    enrollment = Enrollment.objects.get(user=request.user, course_id=course_id)
    if request.method == 'POST':
        course = Course.objects.get(pk=course_id)
        selected_ids = []
        for key in request.POST:
            if key.startswith('choice_'):
                choice_id = request.POST.get(key)
                selected_ids.append(choice_id)

        submission = Submission.objects.create(enrollment=enrollment)
        choices = Choice.objects.filter(id__in=selected_ids)
        submission.choices.set(choices)
        submission.save()

        return redirect('onlinecourse:show_exam_result', course_id=course_id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = Course.objects.get(pk=course_id)
    submission = Submission.objects.get(pk=submission_id)

    score = 0
    total_score = 0
    questions = Question.objects.filter(lesson__course=course)

    for question in questions:
        total_score += question.grade
        selected_choices = submission.choices.filter(question=question)
        if question.is_get_score(selected_choices):
            score += question.grade

    context['course'] = course
    context['submission'] = submission
    context['grade'] = score
    context['total_score'] = total_score
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
