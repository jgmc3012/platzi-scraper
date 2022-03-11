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
        pass

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
    stars = fields.DecimalField(max_digits=2, decimal_places=1)
    writed_at = fields.DatetimeField()
    likes = fields.IntField()
    kind = fields.IntField(
        choices=((tag, tag.value) for tag in Kind)
    )
    class Meta:
        unique_together = ("course", "user")
