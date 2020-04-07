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


class Yearly(NumeratorMixin):
    """ Model without numerator config, default reset mode is yearly """
    id = models.UUIDField(**UUID)
    name = models.CharField(max_length=100)


class Montly(NumeratorMixin):
    """ Model with numerator doc_prefix """

    reset_mode = NumeratorReset.MONTHLY

    id = models.UUIDField(**UUID)
    name = models.CharField(max_length=100)


class CustomFormat(NumeratorMixin):
    doc_prefix = 'CS'
    id = models.UUIDField(**UUID)
    name = models.CharField(max_length=100)

    def get_doc_prefix(self):
        doc_prefix = getattr(self, 'doc_prefix', '')
        return doc_prefix


class Parent1(NumeratorMixin, PolymorphicModel):
    id = models.UUIDField(**UUID)
    name = models.CharField(max_length=100)


class Child1Parent1(Parent1):
    doc_prefix = 'C1'


class Child2Parent1(Parent1):
    doc_prefix = 'C2'


class Parent2(NumeratorMixin, PolymorphicModel):
    doc_prefix = 'P2'
    parent_prefix = True
    parent_model = 'Parent2'
    id = models.UUIDField(**UUID)
    name = models.CharField(max_length=100)


class Child1Parent2(Parent2):
    pass


class Child2Parent2(Parent2):
    pass


class Parent3(PolymorphicModel):
    id = models.UUIDField(**UUID)
    name = models.CharField(max_length=100)


class Child1Parent3(Parent3, NumeratorMixin):
    doc_prefix = 'C1'


class Child2Parent3(Parent3, NumeratorMixin):
    doc_prefix = 'C2'
