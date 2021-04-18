from tortoise import Tortoise
from os import environ

async def init_db():

    await Tortoise.init(
        db_url=environ['DATABASE_URL'],
        modules={'models': [
            'packages.categories.models',
            'packages.careers.models',
            'packages.courses.models',
            ]
        }
    )

    # Generate the schema
    await Tortoise.generate_schemas()
