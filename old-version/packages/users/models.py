from genericpath import exists
from logging import getLogger

from tortoise import fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model
from typing import Tuple, Type, TypeVar

USER = TypeVar("USER", bound="User")
logger = getLogger('log_print')

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    role = fields.CharField(max_length=50)
    name = fields.CharField(max_length=100, null=True)
    public_profile = fields.BooleanField(default=True)
    country_code = fields.CharField(max_length=10, null=True)
    answer_count = fields.IntField(default=0)
    question_count = fields.IntField(default=0)
    rank = fields.IntField(default=0)
    name = fields.CharField(max_length=200, null=True)
    social_medias = fields.ManyToManyField(
        'social_medias.SocialMedia',
        related_name='courses',
        through='social_medias.SocialMediaProfile',
    )
    careers = fields.ManyToManyField('careers.Career', related_name='alumnus')

    def __str__(self):
        return f'User({self.username})'

    @property
    def path(self):
        return f'/p/{self.username}'
    
    async def link_courses(self, course_ids: Tuple[int]):
        logger.debug(f"Link {self.username} with {len(course_ids)} courses")
        # TODO: Use on conflict -> https://stackoverflow.com/questions/41994835/insert-select-from-on-duplicate-key-ignore-postgres
        course_ids_exists = await self.courses.all().values_list('id', flat=True)
        for course_id in set(course_ids) - set(course_ids_exists):
            await self.reviews.create(course_id=course_id)
    
    async def link_careers(self, career_ids: Tuple[int]):
        logger.debug(f"Link {self.username} with {len(career_ids)} careers")
        # TODO: Use on conflict in soft entity
        carrers = await self.careers.related_model.filter(id__in=career_ids)
        await self.careers.add(*carrers)
    
    async def link_social_medias(self, social_media_profiles: Tuple[dict]):
        logger.debug(f"Link {self.username} with {len(social_media_profiles)} social media profiles")
        for social_media_profile in social_media_profiles:
            await self.social_medias.related_model.update_or_create(**social_media_profile)

    async def update(self, **kwargs):
        logger.debug(f"Update User {self.username}")
        await self.update_from_dict(kwargs).save()

    @classmethod
    async def public_profiles(cls):
        return await cls.filter(public_profile=True)

    @classmethod
    async def update_or_create(cls, username: str, **kwargs) -> Tuple[USER, bool]:
        logger.debug(f"Update or create User {username}")
        try:
            user = await cls.get(username=username)
        except DoesNotExist:
            try:
                user = await cls.create(username=username, **kwargs)
                return user, True
            except IntegrityError as err:
                logger.error(f"{err} - Cant Create User ({username})")
                return None, False

        await user.update_from_dict(kwargs).save()
        return user, False

    @classmethod
    async def get_or_create(cls, username: str, **kwargs) -> Tuple[Type[USER], bool]:
        """Get or create user by username

        Args:
            username (str): username of user
            **kwargs: additional fields

        Returns:
            (User, bool): user and created flag
        """
        logger.debug(f"Get or create User {username}")
        try:
            user = await cls.get(username=username)
            return user, False
        except DoesNotExist:
            try:
                user = await cls.create(username=username, **kwargs)
                logger.debug(f"User({user}) created")
                return user, True
            except IntegrityError as err:
                logger.error(f"{err} - Cant Create User ({username})")
                return None, False

    class Meta:
        table = "user_profile"
