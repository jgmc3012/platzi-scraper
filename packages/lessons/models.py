from email.policy import default
from enum import Enum
from tortoise.models import Model
from tortoise import fields

class Lesson(Model):
    id = fields.IntField(pk=True)
    track_number = fields.IntField()
    title = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    course = fields.ForeignKeyField('courses.Course', related_name='lessons')
    duration_in_seg = fields.IntField()

    def get_or_create(self):
        raise NotImplementedError

    def __str__(self):
        return self.name


class Comment(Model):

    class Kind(Enum):
        QUESTION = 1
        SIMPLE = 2

    id = fields.IntField(pk=True)
    lesson = fields.ForeignKeyField('lessons.Lesson', related_name='comments')
    father = fields.ForeignKeyField('lessons.Comment', related_name='chilldrens')
    user = fields.ForeignKeyField('users.User', related_name='comments')
    content = fields.TextField()
    writed_at = fields.DatetimeField()
    likes = fields.IntField()
    kind = fields.IntField(
        choices=((tag, tag.value) for tag in Kind),
        default=Kind.SIMPLE.value
    )
    external_id = fields.CharField(100)

    class Meta:
        unique_together = ("course", "user")

    def get_or_create(self):
        raise NotImplementedError

    def __str__(self):
        return f'{self.user}: {self.content[:20]}...'
