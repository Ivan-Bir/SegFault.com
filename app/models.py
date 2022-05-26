# import django.contrib.auth.models
# import uuid
# from django.db import models
# from django.db.models import Count

# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType


# # Managers
# class QuestionManager(models.Manager):
#     def latest_questions(self, count=5):
#         # return self.all().order_by('-id')[0:5]
#         return self.all().annotate(popular=Count('tags')).order_by('-id')[:count]

#     def popular_questions(self, count=5):
#         # return self.all().order_by('-id')[0:5]
#         return self.all().annotate(popular=Count('question')).order_by('-id')[:count]


# class UsersManager(models.Manager):
#     def active_users(self, count=5):
#         # Profile.objects.all().annotate()
#         return self.annotate(answers_count=Count('answer')).order_by('-answers_count')[:count]


# class TagManager(models.Manager):
#     def popular_tags(self, count=5):
#         return self.all().annotate(popular=Count('tags')).order_by('-popular')[:count]

# # paths

# # def question_directory_path(instance, filename):
# #     return 'question_image/{0}/{1}'.format(str(instance.u_id), filename)


# def user_avatar_directory_path(instance, filename):
#     return 'user_avatars/{0}/{1}'.format(str(instance.u_id), filename)


# # def default_question_image_path():
# #     return 'question_image/default/default_image.jpg'


# def default_user_avatar_path():
#     return 'user_avatars/default/default_avatar.jpg'


# # Models
# class Answer(models.Model):
#     question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer')
#     author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='answer')

#     text = models.TextField()

#     isCorrect = models.BooleanField(default=False)

#     date = models.DateTimeField(auto_now_add=True)

#     likes = GenericRelation('Like')
#     dislikes = GenericRelation('Dislike')

#     def __str__(self):
#         return ' '.join([str(self.id), self.text[:10]])


# class Question(models.Model):
#     # id = models.AutoField(primary_key=True, editable=False)
#     # u_id = models.UUIDField(default=uuid.uuid4, editable=False)

#     author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='question')

#     title = models.CharField(max_length=256)
#     text = models.TextField()
#     # image = models.ImageField(upload_to=question_directory_path, default=default_question_image_path)
#     tags = models.ManyToManyField('Tag', related_name='tags')

#     likes = GenericRelation('Like')
#     dislikes = GenericRelation('Dislike')

#     counter_votes = models.IntegerField(default=0)
#     counter_answers = models.IntegerField(default=0)
#     counter_views = models.IntegerField(default=0)

#     publish_date = models.DateTimeField(auto_now_add=True)
#     objects = QuestionManager()

#     def __str__(self):
#         return ' '.join([str(self.id), self.title])


# class Tag(models.Model):
#     name = models.CharField(max_length=256)

#     objects = TagManager()

#     def __str__(self):
#         return ' '.join([self.name])


# class Profile(models.Model):
#     # id = models.AutoField(primary_key=True, editable=False)
#     u_id = models.UUIDField(default=uuid.uuid4, editable=False)

#     user = models.OneToOneField(django.contrib.auth.models.User, on_delete=models.CASCADE, related_name='profile')
#     # nickname = models.CharField(max_length=256)
#     avatar = models.ImageField(upload_to=user_avatar_directory_path, default=default_user_avatar_path)

#     date = models.DateTimeField(auto_now_add=True)

#     objects = UsersManager()

#     def __str__(self):
#         return ' '.join([str(self.id), self.user.username])


# class Like(models.Model):
#     counter = models.PositiveIntegerField(default=0)
#     users = models.ForeignKey('Profile', related_name='likes', on_delete=models.PROTECT)
#     content_type = models.OneToOneField(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveBigIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return ' '.join(str(self.object_id), str(self.counter))


# class Dislike(models.Model):
#     counter = models.PositiveIntegerField(default=0)
#     users = models.ForeignKey('Profile', related_name='dislikes', on_delete=models.PROTECT)
#     content_type = models.OneToOneField(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveBigIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return ' '.join(str(self.object_id), str(self.counter))

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class ProfileManager(models.Manager):
    def get_top_users(self, count=5):
        return self.annotate(answers_count=Count('answer')).order_by('-answers_count')[:count]


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    #avatar = models.ImageField(upload_to="img/" + str(user) + ".png" , default = "img/fishman.png")
    #registration_date = models.DateTimeField()
    # GENDER = [
    #     ('m', 'Male'),
    #     ('f', 'Female'),
    #     ('o', 'Other')
    # ]
    # gender = models.CharField(max_length=1, choices=GENDER)

    # avatar = models.ImageField(upload_to="img/" + str(user) + ".png" , default = "img/fishman.png")

    # count_questions = models.IntegerField(default=0)
    # count_answers = models.IntegerField(default=0)
    # count_resolved_answers = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"


class TagManager(models.Manager):
    def top_tags(self, count=10):
        return self.annotate(que_count=Count('question')).order_by('-que_count')[:count]


class Tag(models.Model):
    name = models.CharField(max_length=32)
    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def count_answers(self):
        return self.annotate(answers=Count('answer', distinct=True))

    def new(self):
        return self.count_answers().order_by('-publish_date')

    def old(self):
        return self.count_answers().order_by('publish_date')

    def hot(self):
        return self.count_answers().order_by('-rating')

    def by_tag(self, tag):
        return self.count_answers().filter(tags__name=tag)

    def by_id(self, id):
        return self.get(id=id)


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)

    counter_votes = models.IntegerField(default=0)
    counter_answers = models.IntegerField(default=0)
    counter_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    objects = QuestionManager()


class AnswerManager(models.Manager):
    def answer_by_question(self, que_id):
        return self.annotate(likes=Count('likeanswer')) \
            .order_by('publish_date').filter(question_id=que_id)


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    correct = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = AnswerManager()


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
