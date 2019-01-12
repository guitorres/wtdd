from eventex.subscriptions.forms import SubscriptionForm
from django.test import TestCase


class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.form = SubscriptionForm()

    def xtest_form_has_fields(self):
        """Form must have 4 fields"""
        expected = ['name', 'cpf', 'email', 'phone']
        print('oi seu sou o goku', self.form.__dict__)
        self.assertSequenceEqual(expected, list(self.form.fields))
