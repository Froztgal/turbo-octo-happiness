import os

import django
from pydantic import BaseModel, BaseSettings


# Postgres
class PostgresDB(BaseModel):
    user: str
    password: str
    host: str
    port: str
    database: str

    @property
    def DSN(self):
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# Security
class Security(BaseModel):
    secret_key: str
    token_expire: int
    algorithm: str


# Settings
class Settings(BaseSettings):
    app_name: str
    admin_email: str
    security: Security
    postgres_db: PostgresDB
    date_format = "%d.%m.%Y"
    time_format = "%H:%M:%S"

    @property
    def date_time_format(self):
        return f"{self.date_format}, {self.time_format}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


# Singletone
settings = Settings()

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": settings.postgres_db.database,
        "USER": settings.postgres_db.user,
        "PASSWORD": settings.postgres_db.password,
        "HOST": settings.postgres_db.host,
        "PORT": settings.postgres_db.port,
    }
}

INSTALLED_APPS = ("database",)

django.setup()
