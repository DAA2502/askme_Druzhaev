from django.shortcuts import render
from django.core.paginator import Paginator


user = {
    'nickname': '#',
    'email': '#',
    'password': '#'
}

popular_tags = [
    ('Perl', 'success'), ('Python', 'primary'), ('TechnoPark', 'warning'), ('MySQL', 'danger'),
    ('django', 'info'), ('Mail.ru', 'warning'), ('Bootstrap', 'success'), ('FireFox', 'info')
]

tags = []
for i in popular_tags:
    tags.append(i[0])

questions = []
for i in range(30):
    questions.append({
        'title': 'title ' + str(i),
        'id': i,
        'text': 'text' + str(i),
        'tags': tags
    })

answers = []
for i in range(20):
    answers.append({
        'nickname': 'User' + str(i),
        'text': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaa Some text from User' + str(i)
    })

hotQuestions = questions.copy()
hotQuestions.reverse()


def paginator(objects_list, request, per_page = 5):
    page_num = request.GET.get('page')
    paginator = Paginator(objects_list, per_page)
    page = paginator.get_page(page_num)
    return page

def index(request):
    page = paginator(questions, request)
    return render(
        request, 
        'index.html', 
        context = {'user': user, 'tags': popular_tags, 'questions': page.object_list, 'page_obj': page}
        )

def hot(request):
    page = paginator(questions, request)
    return render(
        request, 
        'hot.html', 
        context = {'user': user, 'tags': popular_tags, 'questions': page.object_list, 'page_obj': page}
        )

def tag(request, tag_name):
    page = paginator(questions, request)
    return render(
        request,
        'tags.html',
        context = {'user': user, 'tags': popular_tags, 'tag_name': tag_name, 'questions': page.object_list, 'page_obj': page}
    )

def question(request, question_id):
    page = paginator(answers, request, 3)
    return render(
        request,
        'question.html',
        context = {'user': user, 'tags': popular_tags, 'question': questions[question_id], 'answers': page.object_list, 'page_obj': page}
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