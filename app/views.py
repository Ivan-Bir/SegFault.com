from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "title" : f"Question {i}",
        "text" : f"lorem prismo {i} gji enpwefoefo fwoef oefwefmweifq qw qeqzz sdd",
        "id" : i
    } for i in range(7)

]

def index(request):
    return render(request, 'index.html', {"questions" : QUESTIONS})

def ask(request):
    return render(request, 'ask.html')

def question(request, i:int):
    return render(request, 'question_page.html', {"question" : QUESTIONS[i]})

def log_in(request):
    return render(request, 'log_in.html')

def sign_up(request):
    return render(request, 'sign_up.html')