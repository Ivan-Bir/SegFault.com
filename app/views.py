# from django.shortcuts import render
# from django.core.paginator import Paginator
# from .models import *


# def page_not_found_view(request, exception):
#     content = {
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "not_found_page.html", {"content": content}, status=404)


# # def index(request):
# #     paginator = Paginator(Question.objects.all(), 20)
# #     page = request.GET.get('page')
# #     content = {
# #         'questions': paginator.get_page(page),
# #         "active_users": Profile.objects.active_users,
# #         "popular_tags": Tag.objects.popular_tags,
# #     }
# #     return render(request, "index.html", {"content": content})


# # def question(request, i: int):
# #     paginator = Paginator(Answer.objects.filter(question_id=i), 5)
# #     page = request.GET.get('page')
# #     content = {
# #         "question": Question.objects.get(id=i),
# #         "answers": paginator.get_page(page),
# #         "active_users": Profile.objects.active_users,
# #         "popular_tags": Tag.objects.popular_tags,
# #     }
# #     return render(request, "question_page.html", {"content": content})


# def latest(request):
#     paginator = Paginator(Question.objects.order_by('-id'), 10)
#     page = request.GET.get('page')
#     content = {
#         'questions': paginator.get_page(page),
#         # 'questions': Question.objects.latest_questions,
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "latest.html", {"content": content})


# def popular(request):
#     paginator = Paginator(Question.objects.order_by('author'), 10)
#     page = request.GET.get('page')
#     content = {
#         'questions': paginator.get_page(page),
#         # 'questions': Question.objects.popular_questions,
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "popular.html", {"content": content})


# def tag(request, i: str):
#     paginator = Paginator(Question.objects.filter(tags__name=i), 10)
#     page = request.GET.get('page')
#     content = {
#         'tag': i,
#         'questions': paginator.get_page(page),
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "tag_page.html",
#                   {"content": content})


# def ask(request):
#     content = {
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "ask.html", {"content": content})


# def settings(request):
#     content = {
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "setting_page.html", {"content": content})


# def login(request):
#     content = {
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "log_in.html", {"content": content})


# def signup(request):
#     content = {
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
#     return render(request, "sign_up.html", {"content": content})


from django.shortcuts import redirect, render
from django.http import HttpResponse
from paginator import paginate
from django.core.paginator import Paginator
from app.models import *


top_users = Profile.objects.get_top_users(10)


USER = {"is_auth": False}

# # def index(request):
# #     paginator = Paginator(Question.objects.all(), 20)
# #     page = request.GET.get('page')
# #     content = {
# #         'questions': paginator.get_page(page),
# #         "active_users": Profile.objects.active_users,
# #         "popular_tags": Tag.objects.popular_tags,
# #     }
# #     return render(request, "index.html", {"content": content})


# # def question(request, i: int):
# #     paginator = Paginator(Answer.objects.filter(question_id=i), 5)
# #     page = request.GET.get('page')
# #     content = {
# #         "question": Question.objects.get(id=i),
# #         "answers": paginator.get_page(page),
# #         "active_users": Profile.objects.active_users,
# #         "popular_tags": Tag.objects.popular_tags,
# #     }
# #     return render(request, "question_page.html", {"content": content})

def index(request):
    questions = Question.objects.new()
    page_obj = paginate(questions, request, 10)
    paginator = Paginator(Question.objects.all(), 10)
    page = request.GET.get('page')
    # page_obj = paginator.get_page(page)
    top_tags = Tag.objects.top_tags(10)

    content = {
        # "questions": paginator.get_page(page),
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
    # content = {
    #     "question": Question.objects.get(id=i),
    #     "answers": paginator.get_page(page),
    #     "active_users": Profile.objects.active_users,
    #     "popular_tags": Tag.objects.popular_tags,
    #     "auth": USER['is_auth']
    # }
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
        # "page_title": "Hot questions",
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
        # "page_title": "Hot questions",
        "popular_tags": top_tags,
        "auth": USER['is_auth']
    }

    return render(request, "latest.html", content)


def tag(request, tag: str):
    # questions = Question.objects.by_tag(tag)
    # questions = Question.objects.hot()
    # page_obj = paginate(questions, request, 10)
    content = {
        "tag": tag,
        # "questions": page_obj,
        "active_users": top_users,
        "popular_tags": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    # content = {
#         'tag': i,
#         'questions': paginator.get_page(page),
#         "active_users": Profile.objects.active_users,
#         "popular_tags": Tag.objects.popular_tags,
#     }
    try:
        questions = Question.objects.by_tag(tag)
        # print(questions.count())
        # if (questions.count() == 0):
        #     raise Question.DoesNotExist("questions.count() == 0")
        page_obj = paginate(questions, request, 10)
        content.update({
            "questions": page_obj,
            # "page_title": f"Tag: {tag}",
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
