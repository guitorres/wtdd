from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from eventex.subscriptions.models import Subscription
from django.shortcuts import resolve_url as r


class SubscribeNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))


    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)


    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')


    def test_html(self):
        """Html must contains input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1)
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contains csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')


    def test_has_form(self):
        """Context must have sibscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribeNewPostValid(TestCase):
    def setUp(self):
        data = dict(
            name='Henrique Bastos',
            cpf='12345678901',
            email='henrique@bastos.net',
            phone='21-99618-6180')
        self.resp = self.client.post(r('subscriptions:new'), data)


    def test_post(self):
        """Valid POST should redirect to /inscricao/1/"""
        _hash = Subscription.objects.get(pk=1)._hash
        self.assertRedirects(self.resp, r('subscriptions:detail', _hash))


    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())

class SubscribeNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})


    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)


    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')


    def test_has_form(self):
        """Context must have sibscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())