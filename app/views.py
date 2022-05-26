
from django.shortcuts import redirect, render
from django.http import HttpResponse
from paginator import paginate
from django.core.paginator import Paginator
from app.models import *


top_users = Profile.objects.get_top_users(10)


USER = {"is_auth": False}

def index(request):
    questions = Question.objects.new()
    page_obj = paginate(questions, request, 10)
    top_tags = Tag.objects.top_tags(10)

    content = {
        "questions": page_obj,
        "active_users": top_users,
        "popular_tags": top_tags,
        "auth": USER['is_auth']
    }

    return render(request, "index.html", content)



def ask(request):
    USER['is_auth'] = True
    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    return render(request, "ask.html", content)


def question(request, i: int):
    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    try:
        question = Question.objects.by_id(i)
        answers = paginate(Answer.objects.answer_by_question(i), request, 10)
        content.update({
            "answers": answers,
            "question": question,
        })
    except Exception:
        return render(request, "page_not_found.html", content, status=404)
    return render(request, "question_page.html", content)


def popular(request):
    questions = Question.objects.hot()
    page_obj = paginate(questions, request, 10)
    top_tags = Tag.objects.top_tags(10)
    content = {
        "questions": page_obj,
        "active_users": top_users,
        "popular_tags": top_tags,
        "auth": USER['is_auth']
    }

    return render(request, "popular.html", content)

def latest(request):
    questions = Question.objects.new()
    page_obj = paginate(questions, request, 10)
    top_tags = Tag.objects.top_tags(10)
    content = {
        "questions": page_obj,
        "active_users": top_users,
        "popular_tags": top_tags,
        "auth": USER['is_auth']
    }

    return render(request, "latest.html", content)


def tag(request, tag: str):
    content = {
        "tag": tag,
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    try:
        questions = Question.objects.by_tag(tag)
        page_obj = paginate(questions, request, 10)
        content.update({
            "questions": page_obj,
        })
    except Exception:
        return render(request, "not_found.html", content, status=404)

    return render(request, "tag_page.html", content)


def signup(request):
    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "auth": False
    }
    return render(request, "sign_up.html", content)


def login(request):
    USER['is_auth'] = True
    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    return render(request, "log_in.html", content)


def settings(request):
    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    return render(request, "setting_page.html", content)


def logout(request):
    USER['is_auth'] = False
    return index(request)
