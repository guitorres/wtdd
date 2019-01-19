from django.test import TestCase
from unittest.mock import Mock
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin


class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)
        Subscription.objects.create(name='Henrique Bastos', cpf='12345678901',
                                    email='henrique@bastos.net', phone='21-996186180')
        self.queryset = Subscription.objects.all()
        self.mock = Mock()
        self.old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = self.mock


    def test_has_action(self):
        """Action mark_as_paid should be installed."""
        self.assertIn('mark_as_paid', self.model_admin.actions)


    def test_mark_all(self):
        """It should mark all selected subscriptions as paid."""
        self.model_admin.mark_as_paid(None, self.queryset)
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())
        SubscriptionModelAdmin.message_user = self.old_message_user


    def test_message(self):
        """It should send a message to the user."""
        self.model_admin.mark_as_paid(None, self.queryset)
        self.mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')
        SubscriptionModelAdmin.message_user = self.old_message_user