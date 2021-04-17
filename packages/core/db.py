from tortoise import Tortoise

async def init_db():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['packages.scraper.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
