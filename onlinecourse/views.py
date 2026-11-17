from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def course_details(request, course_id):
    context = {}
    try:
        course = Course.objects.get(pk=course_id)
        context['course'] = course
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    
    if request.method == 'POST':
        # Enrollment get kar rahe hain ya create kar rahe hain current user ke liye
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )
        
       
        submission = Submission.objects.create(enrollment=enrollment)
        
        
        choice_ids = request.POST.getlist('choice')
        for choice_id in choice_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
            
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))
    
    return redirect('onlinecourse:course_details', course_id=course.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
   
    selected_ids = submission.choices.values_list('id', flat=True)
    
    context['course'] = course
    context['submission'] = submission
    context['selected_ids'] = selected_ids  # Context mein add kar diya gaya hai
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
