from django.db.models import CharField, ManyToManyField

from database.mixins.base import BaseMixin
from database.models.role import Role


class Permission(BaseMixin):
    name = CharField(unique=True)
    description = CharField(null=True, blank=True)

    # Relation
    role = ManyToManyField(Role)

    class Meta:
        db_table = "permission"

    def __str__(self):
        return self.name
