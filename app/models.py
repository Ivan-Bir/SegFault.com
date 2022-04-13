from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum


LIKE = '1'
DISLIKE = '-1'

#Managers
class ResolvedQuestions(models.Manager):
    def resolved_questions(self):
        return self.filter(status = True)

class TagManager(models.Manager):
    def top_tags(self, count=10):
        return self.annotate(count=Count('tag_related')).order_by('-count')[:count]

class AnswerManager(models.Manager):
    def answer_by_question(self, id):
        # return self.annotate(likes=Sum('answer_like__mark')).order_by('-likes').filter(question_id=id)
        return self.annotate(likes=Sum('answer_like__mark')).order_by('pub_date').filter(question_id=id)

class QuestionManager(models.Manager):
    def count_answers(self):
        return self.annotate(answers=Count('answer_related', distinct=True))

    def get_by_likes(self):
        return self.count_answers().order_by('-rating')

    def get_by_id(self, id):
        return self.count_answers().get(id=id)

    def by_tag(self, tag):
        return self.count_answers().filter(tags__name=tag)

    def new(self):
        return self.count_answers().order_by('-publicate_date')

    def hot(self):
        return self.get_by_likes()

#begin general classes
class TagQuestion(models.Model):
    name_tag = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name_tag}"



class Answer(models.Model):
    # linked_question = models.ForeignKey(Question, models.CASCADE)

    author = models.CharField(max_length=64)
    text_answer = models.TextField()
    publicate_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    rating_ans = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"{self.publicate_date} {self.author}"

class Question(models.Model):
    title_quest = models.CharField(max_length=255)
    text_quest = models.TextField()
    publicate_date = models.DateTimeField(blank=True, null=True) #DateField
    last_update = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=64)

    tags = models.ManyToManyField(TagQuestion)
    answers = models.ForeignKey(Answer, models.CASCADE, blank=True, null=True)

    rating_quest = models.IntegerField(default=0)
    status = models.BooleanField(blank=True, default=False)

    object = ResolvedQuestions()

    def __str__(self):
        return f"{self.title_quest} {self.text_quest} {self.author} {self.publicate_date}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='profile_related')
    registration_date = models.DateTimeField()
    GENDER = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER)

    avatar = models.ImageField(upload_to="img/" + str(user) + ".png" , default = "img/fishman.png")

    count_questions = models.IntegerField(default=0)
    count_answers = models.IntegerField(default=0)
    count_resolved_answers = models.IntegerField(default=0)

class LikeQuestion(models.Model):
    MARK = [
        (LIKE, 'Like'),
        (DISLIKE, "Dislike"),
    ]
    mark = models.IntegerField(choices=MARK)
    question = models.ForeignKey(Question, related_name="question_like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)


class LikeAnswer(models.Model):
    MARK = [
        (LIKE, 'Like'),
        (DISLIKE, "Dislike"),
    ]
    mark = models.IntegerField(choices=MARK)
    answer = models.ForeignKey(Answer, related_name="answer_like", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)



class QuestionInstance(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    STATUSES = [
        ('m', 'On_moderation'),
        ('p', 'Published'),
        ('b', 'Banned')
    ]
    status = models.CharField(max_length=1, choices=STATUSES, default='m')