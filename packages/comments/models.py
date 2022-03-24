from logging import getLogger
from typing import Tuple, Type, TypeVar

from tortoise import fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model

logger = getLogger('log_print')
COMMENT = TypeVar("COMMENT", bound="Comment")


class Comment(Model):

    id = fields.IntField(pk=True)
    lesson = fields.ForeignKeyField('lessons.Lesson', related_name='comments')
    father = fields.ForeignKeyField(
        'comments.Comment', related_name='chilldrens')
    author = fields.ForeignKeyField('users.User', related_name='comments')
    content = fields.TextField()
    writed_at = fields.DatetimeField()
    likes = fields.IntField()
    external_id = fields.CharField(50)

    def __str__(self):
        return f'Comment({self.author}: {self.content[:20]}...)'

    @classmethod
    async def update_or_create(cls, external_id, **kwargs) -> Tuple[Type[COMMENT], bool]:
        logger.debug(f"Update or create Comment by {kwargs.get('author', external_id)}")
        try:
            comment = await cls.get(external_id=external_id)
        except DoesNotExist:
            try:
                comment = await cls.create(external_id=external_id, **kwargs)
                return comment, True
            except IntegrityError as err:
                logger.error(f"{err} - Cant Create Comment ({kwargs.get('author', external_id)})")
                return None, False

        await comment.update_from_dict(kwargs).save()
        return comment, False
