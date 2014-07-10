from django.core.urlresolvers import reverse
from django.test import TestCase


class SmokeTestCase(TestCase):
    def test_GET_index_returns_200(self):
        url = reverse('index')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_100_percent_code_coverage(self):
        from amtrak_decal_form import wsgi
        assert wsgi
