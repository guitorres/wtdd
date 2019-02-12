from django.test import TestCase
from django.shortcuts import resolve_url as r

class TestTalkList(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('talk_list'))

    def test_get(self):
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/talk_list.html')