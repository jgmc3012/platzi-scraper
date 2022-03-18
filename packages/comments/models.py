from logging import getLogger

from tortoise import fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model

logger = getLogger('log_print')


class Comment(Model):

    id = fields.IntField(pk=True)
    lesson = fields.ForeignKeyField('lessons.Lesson', related_name='comments')
    father = fields.ForeignKeyField(
        'comments.Comment', related_name='chilldrens')
    author = fields.ForeignKeyField('users.User', related_name='comments')
    content = fields.TextField()
    writed_at = fields.DatetimeField()
    likes = fields.IntField()
    external_id = fields.CharField(100)

    def __str__(self):
        return f'Comment({self.author}: {self.content[:20]}...)'

    async def get_or_create(self, lesson, author, content, likes, external_id, father=None):
        logger.debug(f"Get or create Comment by {author}")

        try:
            comment = await self.get(lesson=lesson, external_id=external_id)
            return comment, False
        except DoesNotExist:
            pass

        try:
            comment = await self.create(
                lesson=lesson, author=author, content=content,
                likes=likes, external_id=external_id, father=father
            )
        except IntegrityError as err:
            logger.error(f"{err} - Cant Create Comment ({author})")
            return None, False

        logger.debug(f"{comment} created")
        return comment, True
