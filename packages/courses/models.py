from tortoise.models import Model
from tortoise import fields

class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    path = fields.CharField(max_length=150)
    careers = fields.ManyToManyField('packages.careers.models.Career', related_name='courses')

    def __str__(self):
        return self.name


class Review(Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField('packages.courses.models.Course', related_name='reviews')
    user = fields.ForeignKeyField('packages.users.models.User', related_name='reviews')
    comment = fields.TextField()
    stars = fields.DecimalField(max_digits=2, decimal_places=1)
