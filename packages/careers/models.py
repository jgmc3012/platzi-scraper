from tortoise.models import Model
from tortoise import fields

class Career(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    category = fields.ForeignKeyField('categories.Category', related_name='careers')

    def __str__(self):
        return self.name
