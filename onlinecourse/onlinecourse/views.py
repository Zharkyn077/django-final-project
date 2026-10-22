from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))
        
        if not selected_choice_ids:
            return redirect('onlinecourse:course_details', course_id=course.id)
            
        submission = Submission.objects.create(user=request.user)
        choices = Choice.objects.filter(id__in=selected_choice_ids)
        submission.choices.set(choices)
        submission.save()
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    user_score = 0
    
    for question in course.question_set.all():
        total_score += question.grade
        selected_ids = submission.choices.filter(question=question).values_list('id', flat=True)
        if question.is_get_score(selected_ids):
            user_score += question.grade
            
    percentage = (user_score / total_score) * 100 if total_score > 0 else 0
    passed = percentage >= 70
    
    context = {
        'course': course,
        'submission': submission,
        'user_score': user_score,
        'total_score': total_score,
        'percentage': percentage,
        'passed': passed
    }
    return render(request, 'onlinecourse/exam_result.html', context)
