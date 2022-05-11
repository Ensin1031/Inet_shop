from django.urls import reverse, resolve

from main_app.tests.test_settings import SettingsTestCases
from shopping.views import ShowGood, ShowAllGoods


class ShoppingUrlsTests(SettingsTestCases):
    """Test urls for shopping app"""

    def test_shopping_home_url_response(self):
        response = self.client.get(reverse('shopping'))
        self.assertEqual(200, response.status_code)

    def test_shopping_home_url_is_resolved(self):
        url = reverse('shopping')
        self.assertEqual('shopping/', resolve(url).route)
        self.assertEqual(ShowAllGoods, resolve(url).func.view_class)

    def test_good_url_response(self):
        response = self.client.get(reverse('good', args=[self.test_good.slug]))
        self.assertEqual(200, response.status_code)

    def test_good_url_is_resolved(self):
        url = reverse('good', args=[self.test_good.slug])
        self.assertEqual('shopping/good/<str:slug>/', resolve(url).route)
        self.assertEqual(self.test_good.slug, resolve(url).kwargs['slug'])
        self.assertEqual(ShowGood, resolve(url).func.view_class)

    def test_category_url_response(self):
        response = self.client.get(
            reverse('category', args=[self.test_category.slug]))
        self.assertEqual(200, response.status_code)

    def test_category_url_is_resolved(self):
        url = reverse('category', args=[self.test_category.slug])
        self.assertEqual('shopping/category/<str:slug_cat>/',
                         resolve(url).route)
        self.assertEqual(self.test_category.slug,
                         resolve(url).kwargs['slug_cat'])
        self.assertEqual(ShowAllGoods, resolve(url).func.view_class)

    def test_brand_url_response(self):
        response = self.client.get(
            reverse('brand', args=[self.test_brand.slug]))
        self.assertEqual(200, response.status_code)

    def test_brand_url_is_resolved(self):
        url = reverse('brand', args=[self.test_brand.slug])
        self.assertEqual('shopping/brand/<str:slug_brand>/',
                         resolve(url).route)
        self.assertEqual(self.test_brand.slug,
                         resolve(url).kwargs['slug_brand'])
        self.assertEqual(ShowAllGoods, resolve(url).func.view_class)

    def test_search_result_url_response(self):
        response = self.client.get(reverse('search_result', args=['test']))
        self.assertEqual(200, response.status_code)

    def test_search_result_url_is_resolved(self):
        url = reverse('search_result', args=['test'])
        self.assertEqual('/shopping/search_%22test%22/', url)
