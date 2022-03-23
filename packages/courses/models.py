from logging import getLogger

from tortoise.models import Model
from tortoise import fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from typing import Tuple, Type, TypeVar

COURSE = TypeVar("COURSE", bound="Course")
logger = getLogger('log_print')

class Course(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    careers = fields.ManyToManyField('careers.Career', related_name='courses')
    release = fields.DatetimeField(blank=True, null=True)
    teacher = fields.ForeignKeyField('users.User', related_name='courses', blank=True, null=True)
    external_id = fields.CharField(50, unique=True)
    type = fields.CharField(max_length=50, null=True)

    async def actives(self):
        raise NotImplementedError
    
    @classmethod
    async def update_or_create(cls, external_id, **kwargs)-> Tuple[Type[COURSE], bool]:
        logger.debug(f"Update course {kwargs.get('title', external_id)}")
        try:
            course = await cls.get(external_id=external_id)
        except DoesNotExist:
            try:
                course = await cls.create(external_id=external_id, **kwargs)
            except IntegrityError as err:
                logger.error(f"{err} - Cant Create Course ({kwargs.get('title', external_id)})")
                return None, False
            return course, True

        await course.update_from_dict(kwargs).save()
        return course, False

    def __str__(self):
        return f"Course({self.title})"
