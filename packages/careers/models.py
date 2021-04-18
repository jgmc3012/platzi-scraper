from tortoise.models import Model
from tortoise import fields

class Career(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    path = fields.CharField(max_length=150)
    category = fields.ForeignKeyField('packages.categories.models.Category', related_name='careers')

    def __str__(self):
        return self.name
