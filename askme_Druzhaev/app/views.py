from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *


popular_tags = [
    ('Perl', 'success'), ('Python', 'primary'), ('TechnoPark', 'warning'), ('MySQL', 'danger'),
    ('django', 'info'), ('Mail.ru', 'warning'), ('Bootstrap', 'success'), ('FireFox', 'info')
]

user = Profile.objects.all()[0]
questions = Question.objects.with_answers()
questionLikes = QuestionLike.objects.all()


def paginator(objects_list, request, per_page = 5):
    page_num = request.GET.get('page')
    paginator = Paginator(objects_list, per_page)
    page = paginator.get_page(page_num)
    return page

def index(request):
    questions = Question.objects.order_by_date()
    page = paginator(questions, request)
    return render(
        request, 
        'index.html', 
        context = {'user': user, 'tags': popular_tags, 
                   'questions': page.object_list, 'questionlikes': questionLikes,
                   'page_obj': page}
        )
 
def hot(request):
    page = paginator(questions, request)
    return render(
       request, 
       'hot.html', 
       context = {'user': user, 'tags': popular_tags, 
                  'questions': page.object_list, 'page_obj': page}
       )

def tag(request, tag_name):
    questions = Question.objects.with_tag(Tag.objects.get_tag_id(tag_name))
    page = paginator(questions, request)
    return render(
        request,
        'tags.html',
        context = {'user': user, 'tags': popular_tags, 
                   'tag_name': tag_name, 'questions': page.object_list, 
                   'page_obj': page}
    )

def question(request, question_id):
    answers = Answer.objects.on_question(question_id)
    answerLikes = AnswerLike.objects.all()
    page = paginator(answers, request, 3)
    return render(
        request,
        'question.html',
        context = {'user': user, 'tags': popular_tags, 
                   'question': questions[question_id - 1], 'answers': page.object_list, 
                   'answerlikes': answerLikes, 'page_obj': page}
    )

def ask(request):
    return render(
        request,
        'ask.html',
        context = {'user': user, 'tags': popular_tags}
    )

def login(request):
    return render(
        request,
        'login.html',
        context = {'user': user, 'tags': popular_tags}
    )

def signup(request):
    return render(
        request,
        'signup.html',
        context = {'user': user, 'tags': popular_tags}
    )

def settings(request):
    return render(
        request,
        'settings.html',
        context = {'user': user, 'tags': popular_tags}
    )