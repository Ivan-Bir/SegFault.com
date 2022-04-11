from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

QUESTIONS = []
for i in range(1,10):
    QUESTIONS.append({
    "title": "title " + str(i),
    "id": i,
    "text": "text" + str(i) + "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
})

NAME_TAGS = {"default" : "default_tag", "python" : "Python", "cpp11" : "cpp11", "qt" : "Qt" ,
            "templates" : "Templates", "boost" : "Boost", "pointers" : "Pointers", "c_sharp" : "C_sharp", "cmake" : "Cmake"}

DATA = {"questions" : QUESTIONS, "tags" : NAME_TAGS}

DATA_ONE_QUESTION = {"question" : QUESTIONS[0], "tags" : NAME_TAGS}

def index(request):
    return render(request, 'index.html', {"data" : DATA})

def ask(request):
    return render(request, 'ask.html', {"data" : DATA})

def question(request, i:int):
    return render(request, 'question_page.html', {"data" : DATA_ONE_QUESTION})

def log_in(request):
    return render(request, 'log_in.html', {"data" : DATA})

def sign_up(request):
    return render(request, 'sign_up.html', {"data" : DATA})

def tag(request, name:str):
    return render(request, 'tag_page.html', {"data" : DATA})

def page(request, i:int):
    return render(request, 'index.html', {"data" : DATA})

