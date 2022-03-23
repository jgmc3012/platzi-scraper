from logging import getLogger

from tortoise import fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model

logger = getLogger('log_print')

class Lesson(Model):
    id = fields.IntField(pk=True)
    track_number = fields.IntField()
    title = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)
    course = fields.ForeignKeyField('courses.Course', related_name='lessons')
    duration_in_seg = fields.IntField()
    external_id = fields.CharField(50)
    type = fields.CharField(max_length=50)

    def __str__(self):
        return f"Lesson({self.title})"


    async def get_or_create(self, title, course, path, duration_in_seg, track_number):
        logger.debug(f"Get or create Lesson {title}")
        try:
            lesson = await self.get(title=title, course=course)
            return lesson, False
        except DoesNotExist:
            pass

        try:
            lesson = await self.create(
                title=title, course=course, path=path,
                duration_in_seg=duration_in_seg,
                track_number=track_number
            )
        except IntegrityError as err:
            logger.error(f"{err} - Cant Create Lesson ({title})")
            return None, False

        logger.debug(f"{lesson} created")
        return lesson, True
