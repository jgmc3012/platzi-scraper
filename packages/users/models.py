from logging import getLogger

from tortoise import fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.models import Model

logger = getLogger('log_print')

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

    async def get_or_create(self, username: str):
        """Get or create user by username

        Args:
            username (str): username of user

        Returns:
            (User, bool): user and created flag
        """
        logger.debug(f"Get or create Review by {username}")

        try:
            user = await self.get(username=username)
            return user, False
        except DoesNotExist:
            pass

        try:
            user = await self.create(username=username)
        except IntegrityError as err:
            logger.error(f"{err} - Cant Create User ({username})")
            return None, False

        logger.debug(f"User({user}) created")
        return user, True

    class Meta:
        table = "user_profile"
