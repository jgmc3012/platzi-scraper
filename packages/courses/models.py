from logging import getLogger

from tortoise.models import Model
from tortoise import fields

logger = getLogger('log_print')

class Course(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    careers = fields.ManyToManyField('careers.Career', related_name='courses')
    release = fields.DatetimeField(blank=True, null=True)
    teacher = fields.ForeignKeyField('users.User', related_name='courses', blank=True, null=True)
    external_id = fields.CharField(50)
    type = fields.CharField(max_length=50, unique=True)

    async def actives(self):
        raise NotImplementedError
    
    async def get_or_create(self, external_id, **kwargs):
        try:
            course = await Course.get(external_id=external_id)
            return course, False
        except Course.DoesNotExist:
            course = await Course.create(external_id=external_id, **kwargs)
            return course, True

    def __str__(self):
        return f"Course({self.title})"
