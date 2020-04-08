import uuid
from django.db import models
from django_numerators.models import NumeratorMixin, NumeratorReset

from polymorphic.models import PolymorphicModel

UUID = {
    'default': uuid.uuid4,
    'unique': True,
    'primary_key': True,
    'editable': True
}
