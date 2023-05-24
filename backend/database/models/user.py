from django.db.models import BooleanField, CharField

from database.mixins.base import BaseMixin


class User(BaseMixin):
    user_name = CharField(unique=True)
    email = CharField(unique=True)
    password_hash = CharField()
    is_active = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.user_name
