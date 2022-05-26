# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from app.models import *

# from faker import Faker

# class Command(BaseCommand):
#     faker = Faker()
#     help = 'Generator for database'

#     def handle(self, *args, **options):
#         params = {
#             "USERS": options.get('users'),
#             "QUESTIONS": options.get('questions'),
#             "TAGS": options.get('tags'),
#             "ANSWERS": options.get('answers'),
#         }

#         if options['default']:
#             params["USERS"] = 100
#             params["QUESTIONS"] = 800
#             params["TAGS"] = 30
#             params["ANSWERS"] = 2000

#         print(params)
#         self.create_profiles(params)
#         self.create_tags(params)
#         self.create_questions(params)
#         self.create_answers(params)
#         self.set_tags_to_questions(params)

#     def add_arguments(self, parser):
#         parser.add_argument(
#             '-u',
#             '--users',
#             action='store',
#             default=0,
#             help='Count of generated user profiles'
#         )
#         parser.add_argument(
#             '-q',
#             '--questions',
#             action='store',
#             default=0,
#             help='Count of generated questions'
#         )
#         parser.add_argument(
#             '-t',
#             '--tags',
#             action='store',
#             default=0,
#             help='Count of generated tags'
#         )
#         parser.add_argument(
#             '-a',
#             '--answers',
#             action='store',
#             default=0,
#             help='Count of generated answers'
#         )
#         parser.add_argument(
#             '-d',
#             '--default',
#             action='store_true',
#             default=True,
#             help='Generate a lot of data'
#         )
#         parser.add_argument(
#             '-c',
#             '--clear',
#             action='store_true',
#             default=True,
#             help='Clear database'
#         )

#     def user_generate(self):
#         username = self.faker.unique.user_name()
#         first_name = self.faker.first_name()
#         last_name = self.faker.last_name()
#         email = self.faker.email()
#         password = self.faker.password()
#         user = User(username=username, first_name=first_name,
#                     last_name=last_name, email=email, password=password)
#         return user

#     # def create_profiles(self, params):
#     #     print('Creatings users...')
#     #     usrs_list = list()
#     #     profiles_list = list()
#     #     for i in range(1, params["USERS"] + 1):
#     #         new_us = self.user_generate()
#     #         profiles_to_cr.append(
#     #             Profile(user=new_us,
#     #                     nickname=f'test_nick_{i}'))
#     #         # new_us.save()

#     #     # Create
#     #     print('Creating profiles...')

#     #     for i in range(1, params["USERS"] + 1):
#     #         i+i

#     #     # Save
#     #     Profile.objects.bulk_create(profiles_to_cr, ignore_conflicts=True)

#     def create_profiles(self, params):
#         print('Creatings users...')
#         usrs_list = list()
#         profiles_list = list()
#         for i in range(params["USERS"]):
#             cur_user = self.user_generate()
#             cur_user.save()
#             usrs_list.append(cur_user)
#             profiles_list.append(Profile(user=cur_user))

#         # User.objects.bulk_create(usrs_list)
#         Profile.objects.bulk_create(profiles_list)
#         print("USER DONE")

#     def create_tags(self, params):
#         print('Creatings tags...')
#         tags_to_create = []
#         for i in range(1, params["TAGS"] + 1):
#             tags_to_create.append(Tag(name=fself.faker.word()))
#         Tag.objects.bulk_create(tags_to_create, ignore_conflicts=True)

#     def create_questions(self, params):
#         print('Creatings questions...')
#         questions_to_create = []
#         for i in range(1, params["QUESTIONS"] + 1):
#             questions_to_create.append(Question(title=f'test_Q_{i}',
#                                                 text=f'test_text_{i}',
#                                                 author=Profile.objects.get(
#                                                     nickname=f'test_nick_{max(i % params["USERS"], 1)}'),
#                                                 counter_votes = i*10+2,
#                                                 counter_answers = (i*10+2)/2 + 3,
#                                                 counter_views = i*i + 11
#                                                 ),
#                                        )
#         Question.objects.bulk_create(questions_to_create, ignore_conflicts=True)

#     def set_tags_to_questions(self, params):
#         print('  Setting tags for questions...')
#         questions_to_create = Question.objects.all()
#         for i in range(1, params["QUESTIONS"] + 1):
#             tag = Tag.objects.all().get(name=f'testtag_{i % params["TAGS"] if i % params["TAGS"] else params["TAGS"]}')
#             questions_to_create[i - 1].tags.add(tag)
#         Question.objects.bulk_create(questions_to_create, ignore_conflicts=True)

#     def create_answers(self, params):
#         print('Creating answers...')
#         count = 1000
#         j = 0
#         questions = Question.objects.all()
#         while j < params["ANSWERS"] + 1:
#             print(j, ' ', j + count)
#             answers_to_create = []
#             for i in range(j, j + count):
#                 answers_to_create.append(
#                     Answer(
#                         question=questions[
#                             (i % params["QUESTIONS"] if i % params["QUESTIONS"] else params["QUESTIONS"]) - 1],
#                         author=Profile.objects.get(
#                             nickname=f'test_nick_{i % params["USERS"] if i % params["USERS"] else params["USERS"]}'),
#                         text=f'Test answer {i}',
#                         isCorrect = (i%3 == 0) #
#                         )
#                 )
#             print("try so save")
#             Answer.objects.bulk_create(answers_to_create, ignore_conflicts=True)
#             j += count

from segfault.settings import BASE_DIR
from django.core.management.base import BaseCommand
from app.models import Question, Profile, LikeQuestion, LikeAnswer, Tag, Answer

from faker import Faker
from collections import OrderedDict
import random

from django.contrib.auth.models import User

COUNT_USERS = 101
COUNT_QUESTIONS = 1001
COUNT_ANSWERS = 10001
COUNT_TAGS = 101
LIKES = 20001


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.users_generate(COUNT_USERS)
        self.tags_generate(COUNT_TAGS)
        self.questions_generate(COUNT_QUESTIONS)
        self.answers_generate(COUNT_ANSWERS)
        self.likes_generate(LIKES)
        print("SUCCESS")

    def user_generate(self):
        username = self.faker.unique.user_name()
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self.faker.email()
        password = self.faker.password()
        user = User(username=username, first_name=first_name,
                    last_name=last_name, email=email, password=password)
        return user

    def users_generate(self, count):
        print("START GENERATING USERS")
        # usrs_list = list()
        profiles_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            cur_user = self.user_generate()
            cur_user.save()
            # usrs_list.append(cur_user)
            profiles_list.append(Profile(user=cur_user))

        # User.objects.bulk_create(usrs_list)
        Profile.objects.bulk_create(profiles_list)
        print("USER DONE")

    def tags_generate(self, count):
        print("START GENERATING TAGS")
        tag_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            tag_name = self.faker.word()
            tag_list.append(Tag(name=tag_name))
        Tag.objects.bulk_create(tag_list)
        print("TAGS DONE")

    def questions_generate(self, count):
        print("START GENERATING QUESIONS")
        min_id_prof = Profile.objects.order_by('id')[0].id
        max_id_prof = Profile.objects.order_by('-id')[0].id

        tag_id = Tag.objects.order_by('id')[0].id
        tags_count = Tag.objects.all().count()

        question_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            # tags_count_quiestion = random.randint(1, 5)
            text = self.faker.paragraph(random.randint(7, 20))
            profile_id = random.randint(min_id_prof, max_id_prof)
            title = self.faker.paragraph(random.randint(7, 20))

            title = self.faker.paragraph(1)[:-1] + '?'
            tag_list = list()
            cur_question = Question(
                                    text=text,
                                    title=title,
                                    profile_id=profile_id,
                                    counter_votes = i*10+2,
                                    counter_answers = (i*10+2)/2 + 3,
                                    counter_views = i*i + 11
                                    )
            question_list.append(cur_question)
            question_list[i].save()

        q_list = Question.objects.bulk_create(question_list)
        print("list_ques done")
        min_id_tag = Tag.objects.order_by('id')[0].id
        max_id_tag = Tag.objects.order_by('-id')[0].id
        for i in range(count):
            tags_count_quiestion = random.randint(1, 3)
            # tag_rand_id = random.randint(min_id_prof, max_id_prof)
            for j in range(tags_count_quiestion):
                tag = Tag.objects.get(
                    id=random.randint(min_id_tag, max_id_tag))
                # print("-------------------")

                question_list[i].tags.add(tag)

        print("Question DONE")

    def answers_generate(self, count):
        print("START GENERATING ANSWERS")
        min_id_prof = Profile.objects.order_by('id')[0].id
        max_id_prof = Profile.objects.order_by('-id')[0].id
        min_id_que = Question.objects.order_by('id')[0].id
        max_id_que = Question.objects.order_by('-id')[0].id

        ans_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            text = self.faker.paragraph(random.randint(5, 20))
            profile_id = random.randint(min_id_prof, max_id_prof)
            question_id = random.randint(min_id_que, max_id_que)
            cur_ans = Answer(text=text, question_id=question_id,
                             profile_id=profile_id)
            ans_list.append(cur_ans)
        Answer.objects.bulk_create(ans_list)

    def likes_generate(self, count):
        print("START GENERATING LIKES")
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_question_id = Question.objects.order_by('id')[0].id
        max_question_id = Question.objects.order_by('-id')[0].id
        like_q_list = list()
        for i in range(round(count / 2)):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")

            while True:
                profile_id = random.randint(min_profile_id, max_profile_id)
                question_id = random.randint(min_question_id, max_question_id)
                check = LikeQuestion.objects.filter(
                    question_id=question_id, profile_id=profile_id).count()
                if not check:
                    like_q_list.append(LikeQuestion(
                        question_id=question_id, profile_id=profile_id))
                    break
        # print(f"BULK CREATE LIKES {like_q_list.count()}")
        LikeQuestion.objects.bulk_create(like_q_list)

        like_a_list = list()
        min_ans_id = Answer.objects.order_by('id')[0].id
        max_ans_id = Answer.objects.order_by('-id')[0].id
        for i in range(round(count / 2)):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            while True:
                profile_id = random.randint(min_profile_id, max_profile_id)
                ans_id = random.randint(min_ans_id, max_ans_id)

                check = LikeAnswer.objects. \
                    filter(answer_id=ans_id, profile_id=profile_id).count()
                if not check:
                    like_a_list.append(LikeAnswer(
                        answer_id=ans_id, profile_id=profile_id))
                    break

        # print(f"BULK CREATE LIKES {like_a_list.count()}")
        LikeAnswer.objects.bulk_create(like_a_list)
        print("Likes Done")

