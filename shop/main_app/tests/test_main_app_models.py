from decimal import Decimal

from .test_settings import SettingsTestCases


class PromotionModelTest(SettingsTestCases):
    """Test model PromotionDB"""

    def test_validators_meta(self):
        print('----------test model PromotionDB----------')
        print(self.test_promo._meta.get_field('promo_title').verbose_name, '=',
              self.test_promo.promo_title)
        print(self.test_promo._meta.get_field('is_active').verbose_name, '=',
              self.test_promo.is_active)
        print(self.test_promo._meta.get_field('category').verbose_name, '=',
              self.test_promo.category.all())
        print(self.test_promo._meta.get_field('brand').verbose_name, '=',
              self.test_promo.brand.all())
        print(self.test_promo._meta.get_field('discount').verbose_name, '=',
              self.test_promo.discount)
        print(self.test_promo._meta.get_field('description').verbose_name, '=',
              self.test_promo.description)
        print(self.test_promo._meta.get_field('photo').verbose_name, '=',
              self.test_promo.photo.url)
        print(self.test_promo._meta.get_field('slug').verbose_name, '=',
              self.test_promo.slug)

    def test_valid_is_active_promo(self):
        self.assertEqual(False, self.test_promo.is_active)
        self.test_promo.is_active = True
        self.test_promo.save()
        self.assertEqual(True, self.test_promo.is_active)

    def test_valid_category_by_promo(self):
        self.assertEqual('testCategory',
                         self.test_promo.category.all()[0].title)

    def test_valid_brand_by_promo(self):
        self.assertEqual('testBrand', self.test_promo.brand.all()[0].title)

    def test_valid_discount(self):
        self.assertEqual(Decimal('0.15'), self.test_promo.discount)

    def test_valid_description(self):
        self.assertEqual(
            'TestPromoDescription TestPromoDescription TestPromoDescription',
            self.test_promo.description)

    def test_valid_promo_photo(self):
        self.assertEqual(self.test_image_promo, self.test_promo.photo)

    def test_valid_promo_photo_url(self):
        self.assertEqual('/media' + self.test_image_promo,
                         self.test_promo.photo.url)

    def test_valid_slug(self):
        self.assertEqual('testpromoaction', self.test_promo.slug)
