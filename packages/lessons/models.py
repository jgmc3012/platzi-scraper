from enum import Enum
from logging import getLogger

from tortoise import fields
from tortoise.models import Model

logger = getLogger('log_print')

class Lesson(Model):
    id = fields.IntField(pk=True)
    track_number = fields.IntField()
    title = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    course = fields.ForeignKeyField('courses.Course', related_name='lessons')
    duration_in_seg = fields.IntField()

    def get_or_create(self, title, path, course, duration_in_seg, track_number):
        logger.debug(f"Get or create Lesson {title}")

        raise NotImplementedError

    def __str__(self):
        return self.name


class Comment(Model):

    id = fields.IntField(pk=True)
    lesson = fields.ForeignKeyField('lessons.Lesson', related_name='comments')
    father = fields.ForeignKeyField('lessons.Comment', related_name='chilldrens')
    author = fields.ForeignKeyField('users.User', related_name='comments')
    content = fields.TextField()
    writed_at = fields.DatetimeField()
    likes = fields.IntField()
    external_id = fields.CharField(100)

    class Meta:
        unique_together = ("course", "user")

    def get_or_create(self, lesson, father, author, content, likes, external_id):
        logger.debug(f"Get or create Comment by {author}")

        raise NotImplementedError

    def __str__(self):
        return f'{self.user}: {self.content[:20]}...'
