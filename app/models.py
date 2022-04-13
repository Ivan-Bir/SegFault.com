from django.db import models

# Create your models here.
class TagQuestion(models.Model):
    name_tag = models.CharField(max_length=16)


class Answer(models.Model):
    author = models.CharField(max_length=64)
    text_answer = models.TextField()
    publicate_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    likes_ans = models.CharField(max_length=5)
    dislikes_ans = models.CharField(max_length=5)


class Question(models.Model):
    title_quest = models.CharField(max_length=256)
    text_quest = models.TextField()
    publicate_date = models.DateField(blank=True, null=True)
    author = models.CharField(max_length=64)

    tags = models.ManyToManyField(TagQuestion)
    answers = models.ForeignKey(Answer, models.CASCADE())

    likes_quest = models.CharField(max_length=5)
    dislikes_quest = models.CharField(max_length=5)

    RESOLVE_STATUS []



class QuestionInstance(models.Model):
    question = models.ForeignKey(Question, models.Case)
    STATUSES = [
        ()
    ]
    status = models.CharField(max_length=1, choises=STATUSES)