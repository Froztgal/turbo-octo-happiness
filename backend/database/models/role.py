from django.db.models import CASCADE, CharField, ForeignKey

from database.mixins.base import BaseMixin
from database.models.user import User


class Role(BaseMixin):
    name = CharField(unique=True)
    description = CharField(null=True, blank=True)

    # Relation
    user = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        db_table = "role"

    def __str__(self):
        return self.name
