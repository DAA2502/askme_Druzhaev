from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def get_tag_id(self, name):
        return self.get(tag_name = name).id

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return self.tag_name


class QuestionManager(models.Manager):
    def with_answers(self):
        return self.annotate(num_answers = Count('answer'))
    
    def order_by_date(self):
        return self.order_by('-created_at').annotate(num_answers = Count('answer'))
    
    def order_by_rating(self):
        return self.order_by('-rating').annotate(num_answers = Count('answer'))

    def with_tag(self, id_t):
        return self.filter(tags = id_t).annotate(num_answers = Count('answer'))

class Question(models.Model):
    question_title = models.CharField(max_length=255)
    question_text = models.TextField()
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.question_title
    

class QuestionLike(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'question_id')


class AnswerManager(models.Manager):
    def on_question(self, q_id):
        return self.filter(question_id = q_id)

class Answer(models.Model):
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return (self.user_id.user.username + '_on_' +
                self.question_id.question_title + '_at_' +
                str(self.changed_at.strftime('%Y-%m-%d %H:%M:%S')))
    

class AnswerLike(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'answer_id')