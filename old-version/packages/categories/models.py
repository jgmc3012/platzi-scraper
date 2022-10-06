from asyncio.log import logger
from logging import getLogger
from typing import Tuple, Type, TypeVar

from tortoise import fields
from tortoise.exceptions import TransactionManagementError
from tortoise.models import Model

CATEGORY = TypeVar("CATEGORY", bound="Category")
logger = getLogger('log_print')


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    path = fields.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    async def get_or_create(cls, **kwargs) -> Tuple[Type[CATEGORY], bool]:
        try:
            return await super().get_or_create(**kwargs)
        except TransactionManagementError as e:
            for key, value in kwargs.items():
                if await cls.exists(**{key: value}):
                    logger.error(
                        f"Category with the '{key}' equal to '{value}' already exists on DB")
                    break
