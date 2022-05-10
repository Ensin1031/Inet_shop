from main_app.tests.test_settings import SettingsTestCases


class ShopUserModelTest(SettingsTestCases):
    """test model ShopUser"""
    def test_validators_meta(self):
        print('----------test model ShopUser----------')
        print(self.test_user._meta.get_field('password').verbose_name, '=', self.test_user.password)
        print(self.test_user._meta.get_field('last_login').verbose_name, '=', self.test_user.last_login)
        print(self.test_user._meta.get_field('username').verbose_name, '=', self.test_user.username)
        print(self.test_user._meta.get_field('first_name').verbose_name, '=', self.test_user.first_name)
        print(self.test_user._meta.get_field('middle_name').verbose_name, '=', self.test_user.middle_name)
        print(self.test_user._meta.get_field('last_name').verbose_name, '=', self.test_user.last_name)
        print(self.test_user._meta.get_field('email').verbose_name, '=', self.test_user.email)
        print(self.test_user._meta.get_field('is_superuser').verbose_name, '=', self.test_user.is_superuser)
        print(self.test_user._meta.get_field('is_staff').verbose_name, '=', self.test_user.is_staff)
        print(self.test_user._meta.get_field('is_active').verbose_name, '=', self.test_user.is_active)
        print(self.test_user._meta.get_field('is_activated').verbose_name, '=', self.test_user.is_activated)
        print(self.test_user._meta.get_field('date_joined').verbose_name, '=', self.test_user.date_joined)

    def test_valid_password(self):
        self.assertEqual('testPassword', self.test_user.password)

    def test_valid_last_login(self):
        self.assertEqual(None, self.test_user.last_login)

    def test_valid_username(self):
        self.assertEqual('testUser', self.test_user.username)

    def test_valid_first_name(self):
        self.assertEqual('TestFirstName', self.test_user.first_name)

    def test_valid_middle_name(self):
        self.assertEqual(None, self.test_user.middle_name)

    def test_valid_last_name(self):
        self.assertEqual('TestLastName', self.test_user.last_name)

    def test_valid_email(self):
        self.assertEqual('testemail@mail.ru', self.test_user.email)

    def test_valid_is_superuser(self):
        self.assertEqual(False, self.test_user.is_superuser)

    def test_valid_is_staff(self):
        self.assertEqual(False, self.test_user.is_staff)

    def test_valid_is_active(self):
        self.assertEqual(True, self.test_user.is_active)

    def test_valid_is_activated(self):
        self.assertEqual(True, self.test_user.is_activated)

    def test_valid_date_joined(self):
        self.assertEqual(self.test_date, self.test_user.date_joined.date())
