from tortoise.models import Model
from tortoise import fields

class Career(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    path = fields.TextField()
