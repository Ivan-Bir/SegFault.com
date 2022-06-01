
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from pkg_resources import require
from paginator import paginate
from django.core.paginator import Paginator
from app.models import *

from django.contrib import auth
from app.forms import LoginForm,  QuestionForm, SettingsForm, SignUpForm, AnswerForm
from django.core.cache import cache
from segfault.settings import LOGIN_URL
from django.views.decorators.http import require_http_methods

from django.contrib.auth.decorators import login_required

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



@login_required(login_url="login", redirect_field_name="continue")
def ask(request):
    if request.method == "GET":
        form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            profile = Profile.objects.get(id=request.user.id)
            question = form.save(profile)

            return redirect(f"../question/{question.id}")

    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "form" : form
    }

    return render(request, "ask.html", content)


def question(request, i: int):
    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
    }
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f'{LOGIN_URL}?continue={request.path}')
        else:
            form = AnswerForm(data=request.POST)
            if (form.is_valid):
                ans = form.save(commit=False)
                profile = Profile.objects.get(id=request.user.id)
                question = Question.objects.get(id=i)
                ans.profile = profile
                ans.question = question
                ans.save()

                answers = Paginator(Answer.objects.answer_by_question(i), 10)
                return redirect(f"{request.path}?page={answers.num_pages}#{ans.id}")

    if request.method == "GET":
        try:
            question = Question.objects.by_id(i)
            answers = paginate(Answer.objects.answer_by_question(i), request, 10)
            form = AnswerForm()
            content.update({
                "answers": answers,
                "question": question,
                "form": form
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
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "GET":
        form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            auth.login(request, profile.user)
            return redirect("index")

    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "form": form
    }
    return render(request, "sign_up.html", content)


def login(request):
    next = request.GET.get("continue")
    if not next:
        next = "index"

    if request.user.is_authenticated:
        return redirect(next)
    if request.method == "GET":
        form = LoginForm()
        cache.set("continue", next)
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)

            if user:
                auth.login(request, user)

                next_url = cache.get('continue')
                if not next_url:
                    next_url = "index"

                cache.delete('continue')
                return redirect(next_url)
            else:
                form.add_error(None, "Invalid password or login!")
                form.add_error('username', "")
                form.add_error('password', "")

    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "form": form
    }
    return render(request, "log_in.html", content)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == "GET":
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        form = SettingsForm(initial=initial_data)
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("settings")
# def settings(request):
#     if request.method == "GET":
#         initial_data = model_to_dict(request.user)
#         initial_data['avatar'] = request.user.profile.avatar
#         form = SettingsForm(initial=initial_data)
#     if request.method == "POST":
#         initial_data = request.POST
#         instance = request.user
#         form = SettingsForm(request.POST, instance=instance, files=request.FILES)
#         if form.is_valid():  # add check existing
#             form.save()
#             return redirect("settings")

    content = {
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "form": form,
    }

    return render(request, "setting_page.html", content)


@login_required(login_url="login", redirect_field_name="continue")
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="login", redirect_field_name="continue")
def like_question(request):
    question_id = request.POST['question_id']
    print(question_id)
    question = Question.objects.get(id=question_id)
    question.like(request.user.profile_related)
    return JsonResponse({'likes': question.count_likes()})
