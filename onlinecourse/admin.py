from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
