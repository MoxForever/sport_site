from models.api import Settings


TORTOISE_ORM = {
    "connections": {"default": Settings().DB_URL},
    "apps": {
        "models": {
            "models": ["models.db", "aerich.models"],
            "default_connection": "default",
        },
    },
}
