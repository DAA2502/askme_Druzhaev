from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth.models import User
from app import models
from itertools import islice
import random


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int)

    def insert_list(type, model_list):
        batch_size = 10000
        while True:
            batch = list(islice(model_list, batch_size))
            if not batch:
                break
            type.objects.bulk_create(batch, batch_size)

    def handle(self, *args, **options):
        ratio = options['ratio'][0]

        User.objects.all().delete()
        models.Tag.objects.all().delete()
        print('All tables were flushed.')
        print('Generating new records...')

        users = [User(username = f'User_{i+1}') for i in range(ratio)]
        User.objects.bulk_create(users, ratio)
        print(f'Added {ratio} records in table \'Users\'')

        users = User.objects.all()

        profiles = [models.Profile(user = users[i]) for i in range(ratio)]
        models.Profile.objects.bulk_create(profiles, ratio)
        print(f'Added {ratio} records in table \'Profiles\'')

        tags = [models.Tag(tag_name = f'Tag_{i+1}') for i in range(ratio)]
        models.Tag.objects.bulk_create(tags, ratio)
        print(f'Added {ratio} records in table \'Tags\'')

        profiles = models.Profile.objects.all()

        questions = [models.Question(question_title = f'Question_{i+1}',
                                     question_text = f'Some text in question_{i+1}',
                                     user_id = profiles[random.randint(0, len(profiles) - 1)])
                                     for i in range(ratio * 10)]
        models.Question.objects.bulk_create(questions, ratio)

        tags = models.Tag.objects.all()
        questions = list(models.Question.objects.all())

        for question in questions:
            tags_to_add = []
            for i in range(3):
                tags_to_add.append(tags[random.randint(0, len(tags) - 1)])
            question.tags.set(tags_to_add)
            tags_to_add.clear()
        # models.Question.objects.bulk_update(questions)
        print(f'Added {ratio*10} records in table \'Questions\'')

        questions = models.Question.objects.all()

        questions_likes = []
        for i in range(ratio):
            for j in range(100):
                questions_likes.append(models.QuestionLike(user_id = profiles[i],
                                                        question_id = questions[j],
                                                        rating = random.randint(0, 2) - 1))
        models.QuestionLike.objects.bulk_create(questions_likes, ratio)
        print(f'Added {ratio*100} records in table \'QuestionLikes\'')
        
        answers = [models.Answer(answer_text = 'This is an answer on question.',
                                 user_id = profiles[random.randint(0, len(profiles) - 1)],
                                 question_id = questions[random.randint(0, len(questions) - 1)])
                                 for i in range(ratio * 100)]
        models.Answer.objects.bulk_create(answers, ratio)
        print(f'Added {ratio*100} records in table \'Answers\'')

        answers = models.Answer.objects.all()

        answers_likes = []
        for i in range(ratio):
            for j in range(100):
                answers_likes.append(models.AnswerLike(user_id = profiles[i],
                                    answer_id = answers[j],
                                    rating = random.randint(0, 2) - 1))
        models.AnswerLike.objects.bulk_create(answers_likes, ratio)
        print(f'Added {ratio*100} records in table \'AnswerLikes\'')

        print('Completed!')