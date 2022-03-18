from logging import getLogger

from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model
from tortoise import fields

logger = getLogger('log_print')


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