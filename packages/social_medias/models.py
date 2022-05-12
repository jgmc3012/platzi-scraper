from logging import getLogger

from tortoise import fields
from tortoise.models import Model
from typing import TypeVar, Union
from tortoise.exceptions import DoesNotExist, IntegrityError

SOCIAL_MEDIA = TypeVar("SOCIAL_MEDIA", bound="SocialMedia")
logger = getLogger('log_print')

class SocialMedia(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    base_url = fields.CharField(max_length=100, unique=True)


class SocialMediaProfile(Model):
    id = fields.IntField(pk=True)
    social_media = fields.ForeignKeyField('social_medias.SocialMedia', related_name='profiles')
    username = fields.CharField(max_length=100)
    user = fields.ForeignKeyField('users.User')
    external_id = fields.CharField(max_length=100)

    @classmethod
    async def update_or_create(cls, social_media: Union[str, SocialMedia], user, external_id: str):
        if isinstance(social_media, str):
            social_media, _ = await SocialMedia.get_or_create(name=social_media)

        try:
            return await cls.get(
                social_media=social_media,
                user=user
            )
        except DoesNotExist:
            pass

        try:
            return await cls.create(
                social_media=social_media,
                user=user,
                external_id=external_id
            )
        except IntegrityError as e:
            logger.error(f'Error while creating social media profile to {user}: {e}')
            return None
