from tortoise.models import Model
from tortoise import fields

class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    path = fields.TextField()
