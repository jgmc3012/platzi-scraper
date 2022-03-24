from tortoise import Tortoise
from os import environ

APPS = [
    'categories',
    'careers',
    'courses',
    'users',
    'lessons',
    'reviews',
    'comments'
]

THIRD_PARTY_APPS = [
    'aerich',
]

TORTOISE_ORM = {
    "connections": {"default": environ['DATABASE_URL']},
    "apps": {
            **{app: {"models": [f'packages.{app}.models'], "default_connection": "default"} for app in APPS},
            **{app: {"models": [f'{app}.models'], "default_connection": "default"} for app in THIRD_PARTY_APPS},
        },
}

async def init_db():

    await Tortoise.init(
        db_url=TORTOISE_ORM['connections']['default'],
        modules={
            **{app: [f'packages.{app}.models'] for app in APPS},
            **{app: [f'{app}.models'] for app in THIRD_PARTY_APPS}
        }
    )

    # Generate the schema
    await Tortoise.generate_schemas()
