from logging import getLogger

from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model
from tortoise import fields

logger = getLogger('log_print')

class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    careers = fields.ManyToManyField('careers.Career', related_name='courses')
    # release = fields.DatetimeField()
    # teacher = fields.ForeignKeyField('users.User', related_name='courses')

    async def actives(self):
        raise NotImplementedError

    def __str__(self):
        return f"Course({self.name})"


class Review(Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField('courses.Course', related_name='reviews')
    user = fields.ForeignKeyField('users.User', related_name='reviews')
    comment = fields.TextField()
    stars = fields.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        unique_together = ("course", "user")

    async def get_or_create(self, course, user, comment, starts):
        try:
            review = await self.get(
                course=course,
                user=user,
            )
            logger.info(f"Review Exist - User ({user}) to course({course}) ")
            return review, False
        except DoesNotExist:
            pass

        try:
            review = await Review.create(
                course=course,
                user=user,
                comment=comment,
                stars=starts
            )
        except IntegrityError as err:
            logger.error(f"{err} - Cant Link User({user}) with the Course({course}) ")
            return None, False

        logger.debug(f"Linked user({user}) to course({course}) ")
        return review, True