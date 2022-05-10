from django.urls import reverse, resolve

from main_app.views import MainPageView, SearchGoodView, CartShowView
from main_app.tests.test_settings import SettingsTestCases


class MainAppUrlsTests(SettingsTestCases):
    """test urls for main_app app"""
    def test_home_url_response(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(200, response.status_code)

    def test_home_url_is_resolved(self):
        url = reverse('index')
        self.assertEqual('', resolve(url).route)
        self.assertEqual(MainPageView, resolve(url).func.view_class)
