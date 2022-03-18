from logging import getLogger

from tortoise.models import Model
from tortoise import fields

logger = getLogger('log_print')

class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    careers = fields.ManyToManyField('careers.Career', related_name='courses')
    release = fields.DatetimeField(blank=True, null=True)
    teacher = fields.ForeignKeyField('users.User', related_name='courses', blank=True, null=True)

    async def actives(self):
        raise NotImplementedError

    def __str__(self):
        return f"Course({self.name})"
