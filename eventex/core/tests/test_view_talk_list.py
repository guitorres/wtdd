from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.core.models import Talk

class TestTalkList(TestCase):
    def setUp(self):
        Talk.objects.create(
            title='Título da Palestra', start='10:00',
            description='Descrição da palestra.'
        )
        Talk.objects.create(
            title='Título da Palestra', start='13:00',
            description='Descrição da palestra.'
        )

        self.resp = self.client.get(r('talk_list'))

    def test_get(self):
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/talk_list.html')

    def test_html(self):
        contents = [
            (2, 'Título da Palestra'),
            (1, '10:00'),
            (1, '13:00'),
            (2, '/palestrantes/henrique-bastos/'),
            (2, 'Henrique Bastos'),
            (2, 'Descrição da palestra.'),
        ]
        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def text_context(self):
        variables = ['morning_talks', 'afternoon_talks']
        for key in variables:
            with self.subTest():
                self.assertContains(key, self.resp.context)