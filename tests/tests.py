from django.utils import timezone
from django.test import TestCase
from tests.models import (
    Yearly, Montly, CustomFormat,
    Child1Parent1, Child2Parent1,
    Child1Parent2, Child2Parent2,
    Child1Parent3, Child2Parent3
)


class TestNumeratedModel(TestCase):

    def test_yearly_reset_autonumber_concistency(self):
        created_at = timezone.datetime(2019, 1, 31, 0, 0, 0)
        obj1 = Yearly(name='year', created_at=created_at)
        obj1.save()
        self.assertEqual(obj1.inner_id, '19010001')
        obj1.delete()

        obj2 = Yearly(name='year', created_at=created_at)
        obj2.save()
        self.assertEqual(obj2.inner_id, '19010002')

        created_at = timezone.datetime(2020, 1, 31, 0, 0, 0)
        obj3 = Yearly(name='year', created_at=created_at)
        obj3.save()
        self.assertEqual(obj3.inner_id, '20010001')

    def test_montly_reset_autonumber_concistency(self):
        created_at = timezone.datetime(2019, 1, 1, 0, 0, 0)
        obj1 = Montly(name='month', created_at=created_at)
        obj1.save()
        self.assertEqual(obj1.inner_id, '19010001')
        obj1.delete()

        obj2 = Montly(name='month', created_at=created_at)
        obj2.save()
        self.assertEqual(obj2.inner_id, '19010002')

        created_at = timezone.datetime(2019, 2, 1, 0, 0, 0)
        obj3 = Montly(name='month', created_at=created_at)
        obj3.save()
        self.assertEqual(obj3.inner_id, '19020001')

    def test_custom_doc_prefix(self):
        created_at = timezone.datetime(2019, 1, 1, 0, 0, 0)
        obj = CustomFormat(name='CS', created_at=created_at)
        obj.save()
        self.assertEqual(obj.inner_id, 'CS19010001')

    def test_doc_prefix_in_polymorphic_child_model(self):
        created_at = timezone.datetime(2019, 1, 1, 0, 0, 0)
        child_1 = Child1Parent1(name='Child1', created_at=created_at)
        child_1.save()
        self.assertEqual(child_1.inner_id, 'C119010001')

        child_2 = Child2Parent1(name='Child2', created_at=created_at)
        child_2.save()
        self.assertEqual(child_2.inner_id, 'C219010001')

    def test_doc_prefix_in_polymorphic_parent_model(self):
        created_at = timezone.datetime(2019, 1, 1, 0, 0, 0)
        child_1 = Child1Parent2(name='Child1', created_at=created_at)
        child_1.save()
        self.assertEqual(child_1.inner_id, 'P219010001')

        child_2 = Child2Parent2(name='Child2', created_at=created_at)
        child_2.save()
        self.assertEqual(child_2.inner_id, 'P219010002')

    def test_numerator_mixin_in_polymorphic_child_model(self):
        created_at = timezone.datetime(2019, 1, 1, 0, 0, 0)
        child_1 = Child1Parent3(name='Child1', created_at=created_at)
        child_1.save()
        self.assertEqual(child_1.inner_id, 'C119010001')

        child_2 = Child2Parent3(name='Child2', created_at=created_at)
        child_2.save()
        self.assertEqual(child_2.inner_id, 'C219010001')
