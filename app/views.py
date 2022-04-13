from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

QUESTIONS = []
for i in range(1,100):
    QUESTIONS.append({
    "title": "title " + str(i),
    "id": i,
    "text": "text" + str(i) + "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
})

NAME_TAGS = {"default" : "default_tag", "python" : "Python", "cpp11" : "cpp11", "qt" : "Qt" ,
            "templates" : "Templates", "boost" : "Boost", "pointers" : "Pointers", "c_sharp" : "C_sharp", "cmake" : "Cmake"}

DATA = {"questions" : QUESTIONS, "tags" : NAME_TAGS}


def GetOneQuestion(i:int):
    return {"question" : QUESTIONS[i%100], "tags" : NAME_TAGS}

def GetRangeQuestions(index_begin:int, number:int):
    return {"questions" : QUESTIONS[(((index_begin%100-1)*number)%100) : (((index_begin%100)*number)%100)] , "tags" : NAME_TAGS}

def GetOnlyTags():
    return {"question" : [], "tags" : NAME_TAGS}


# begin views functions
def index(request):
    return render(request, 'index.html', {"data" : GetRangeQuestions(1,10)})

def ask(request):
    return render(request, 'ask.html', {"data" : GetOnlyTags()})

def question(request, i:str):
    if not i.isdigit():
        return index(request)
    return render(request, 'question_page.html', {"data" : GetOneQuestion(int(i))})

def log_in(request):
    return render(request, 'log_in.html', {"data" : GetOnlyTags()})

def sign_up(request):
    return render(request, 'sign_up.html', {"data" : GetOnlyTags()})

def settings(request, user:str):
    return render(request, 'setting_page.html', {"data" : GetOnlyTags()})

def tag(request, name:str):
    return render(request, 'tag_page.html', {"data" : DATA})

def page(request, i:str):
    if not i.isdigit():
        return index(request)
    return render(request, 'index.html', {"data" : GetRangeQuestions(int(i),10)})

