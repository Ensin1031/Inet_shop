from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, resolve

from main_app.tests.test_settings import SettingsTestCases


class AccountsUrlsTests(SettingsTestCases):
    """Test urls for accounts app"""

    def test_login_url_response(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(200, response.status_code)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual('accounts/login/', resolve(url).route)
        self.assertEqual(LoginView, resolve(url).func.view_class)

    def test_logout_url_response(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(302, response.status_code)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEqual('accounts/logout/', resolve(url).route)
        self.assertEqual(LogoutView, resolve(url).func.view_class)
