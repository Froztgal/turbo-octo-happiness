from django.db.models import CASCADE, CharField, Model, OneToOneField

from .user import User


class UserInfo(Model):
    first_name = CharField()
    last_name = CharField()
    avatar = CharField()
    phone_number = CharField(unique=True)

    # Relation
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        primary_key=True,
    )

    # Property
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "user_info"

    def __str__(self):
        return self.fullname
