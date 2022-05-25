from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *


def page_not_found_view(request, exception):
    content = {
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "not_found_page.html", {"content": content}, status=404)


def index(request):
    paginator = Paginator(Question.objects.all(), 20)
    page = request.GET.get('page')
    content = {
        'questions': paginator.get_page(page),
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "index.html", {"content": content})


def question(request, i: int):
    paginator = Paginator(Answer.objects.filter(question_id=i), 5)
    page = request.GET.get('page')
    content = {
        "question": Question.objects.get(id=i),
        "answers": paginator.get_page(page),
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "question_page.html", {"content": content})


def latest(request):
    paginator = Paginator(Question.objects.order_by('-id'), 10)
    page = request.GET.get('page')
    content = {
        'questions': paginator.get_page(page),
        # 'questions': Question.objects.latest_questions,
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "latest.html", {"content": content})


def popular(request):
    paginator = Paginator(Question.objects.order_by('author'), 10)
    page = request.GET.get('page')
    content = {
        'questions': paginator.get_page(page),
        # 'questions': Question.objects.popular_questions,
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "popular.html", {"content": content})


def tag(request, i: str):
    paginator = Paginator(Question.objects.filter(tags__name=i), 10)
    page = request.GET.get('page')
    content = {
        'tag': i,
        'questions': paginator.get_page(page),
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "tag_page.html",
                  {"content": content})


def ask(request):
    content = {
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "ask.html", {"content": content})


def settings(request):
    content = {
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "setting_page.html", {"content": content})


def login(request):
    content = {
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "log_in.html", {"content": content})


def signup(request):
    content = {
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "sign_up.html", {"content": content})
