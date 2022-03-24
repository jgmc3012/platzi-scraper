from datetime import datetime
from logging import getLogger
from typing import Tuple, Type, TypeVar

from tortoise import fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model

LESSON = TypeVar("LESSON", bound="Lesson")
logger = getLogger('log_print')


class Lesson(Model):
    id = fields.IntField(pk=True)
    track_number = fields.IntField()
    title = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    course = fields.ForeignKeyField('courses.Course', related_name='lessons')
    duration_in_seg = fields.IntField()
    external_id = fields.CharField(50)
    type = fields.CharField(max_length=50)

    def __str__(self):
        return f"Lesson({self.title})"

    @classmethod
    async def actives(cls):
        return await cls.filter(course__release__lte=datetime.now())

    @classmethod
    async def get_or_create(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    async def update_or_create(cls, external_id, **kwargs) -> Tuple[Type[LESSON], bool]:
        logger.debug(
            f"Update or create Lesson {kwargs.get('title', external_id)}")
        try:
            lesson = await cls.get(external_id=external_id)
        except DoesNotExist:
            try:
                lesson = await cls.create(external_id=external_id, **kwargs)
                return lesson, True
            except IntegrityError as err:
                logger.error(
                    f"{err} - Cant Create Lesson ({kwargs.get('title', external_id)})")
                return None, False

        await lesson.update_from_dict(kwargs).save()
        return lesson, False
