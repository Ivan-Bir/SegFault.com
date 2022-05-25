import django.contrib.auth.models
import uuid
from django.db import models
from django.db.models import Count

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Managers
class QuestionManager(models.Manager):
    def latest_questions(self, count=5):
        # return self.all().order_by('-id')[0:5]
        return self.all().annotate(popular=Count('tags')).order_by('-id')[:count]

    def popular_questions(self, count=5):
        # return self.all().order_by('-id')[0:5]
        return self.all().annotate(popular=Count('question')).order_by('-id')[:count]


class UsersManager(models.Manager):
    def active_users(self, count=5):
        # Profile.objects.all().annotate()
        return self.annotate(answers_count=Count('answer')).order_by('-answers_count')[:count]


class TagManager(models.Manager):
    def popular_tags(self, count=5):
        return self.all().annotate(popular=Count('tags')).order_by('-popular')[:count]

# paths

def question_directory_path(instance, filename):
    return 'question_image/{0}/{1}'.format(str(instance.u_id), filename)


def user_avatar_directory_path(instance, filename):
    return 'user_avatars/{0}/{1}'.format(str(instance.u_id), filename)


def default_question_image_path():
    return 'question_image/default/default_image.jpg'


def default_user_avatar_path():
    return 'user_avatars/default/default_avatar.jpg'


# Models
class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer')
    author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='answer')

    text = models.TextField()

    isCorrect = models.BooleanField(default=False)

    # date = models.DateTimeField(auto_now_add=True)

    likes = GenericRelation('Like')
    dislikes = GenericRelation('Dislike')

    def __str__(self):
        return ' '.join([str(self.id), self.text[:10]])


class Question(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    u_id = models.UUIDField(default=uuid.uuid4, editable=False)

    author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='question')

    title = models.CharField(max_length=256)
    text = models.TextField()
    # image = models.ImageField(upload_to=question_directory_path, default=default_question_image_path)
    tags = models.ManyToManyField('Tag', related_name='tags')

    # date = models.DateTimeField(auto_now_add=True)

    likes = GenericRelation('Like')
    dislikes = GenericRelation('Dislike')

    # counter_votes = models.IntegerField(default=0)
    # counter_answers = models.IntegerField(default=0)
    # counter_ve = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return ' '.join([str(self.id), self.title])


class Tag(models.Model):
    name = models.CharField(max_length=256)

    objects = TagManager()

    def __str__(self):
        return ' '.join([self.name])


class Profile(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    u_id = models.UUIDField(default=uuid.uuid4, editable=False)

    user = models.OneToOneField(django.contrib.auth.models.User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=256)
    avatar = models.ImageField(upload_to=user_avatar_directory_path, default=default_user_avatar_path)

    # date = models.DateTimeField(auto_now_add=True)

    objects = UsersManager()

    def __str__(self):
        return ' '.join([str(self.id), self.nickname])


class Like(models.Model):
    counter = models.PositiveIntegerField(default=0)
    users = models.ForeignKey('Profile', related_name='likes', on_delete=models.PROTECT)
    content_type = models.OneToOneField(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return ' '.join(str(self.object_id), str(self.counter))


class Dislike(models.Model):
    counter = models.PositiveIntegerField(default=0)
    users = models.ForeignKey('Profile', related_name='dislikes', on_delete=models.PROTECT)
    content_type = models.OneToOneField(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return ' '.join(str(self.object_id), str(self.counter))
