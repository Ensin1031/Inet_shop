from decimal import Decimal

from main_app.tests.test_settings import SettingsTestCases


class CategoryModelTest(SettingsTestCases):
    """Test model CategoryDB"""

    def test_validators_meta(self):
        print('----------test model CategoryDB----------')
        print('-------test category parent-------')
        print(self.test_category_parent._meta.get_field('title').verbose_name,
              '=',
              self.test_category_parent.title)
        print(self.test_category_parent._meta.get_field('slug').verbose_name,
              '=',
              self.test_category_parent.slug)
        print(self.test_category_parent._meta.get_field('parent').verbose_name,
              '=',
              self.test_category_parent.parent)
        print('-------test category child-------')
        print(self.test_category._meta.get_field('title').verbose_name, '=',
              self.test_category.title)
        print(self.test_category._meta.get_field('slug').verbose_name, '=',
              self.test_category.slug)
        print(self.test_category._meta.get_field('parent').verbose_name, '=',
              self.test_category.parent)

    def test_valid_category_parent_slug(self):
        self.assertEqual('testcategoryparent', self.test_category_parent.slug)

    def test_valid_category_child_slug(self):
        self.assertEqual('testcategory', self.test_category.slug)

    def test_valid_parent_category_for_parent(self):
        self.assertEqual(None, self.test_category_parent.parent)

    def test_valid_parent_category_for_child(self):
        self.assertEqual('testCategoryParent', self.test_category_parent.title)

    def test_valid_category_by_many_to_many_field_in_promo(self):
        self.assertEqual('testPromoAction',
                         self.test_category.from_category.all()[0].promo_title)


class BrandModelTest(SettingsTestCases):
    """Test model BrandDB"""

    def test_validators_meta(self):
        print('----------test model BrandDB----------')
        print(self.test_brand._meta.get_field('title').verbose_name, '=',
              self.test_brand.title)
        print(self.test_brand._meta.get_field('slug').verbose_name, '=',
              self.test_brand.slug)

    def test_valid_slug(self):
        self.assertEqual('testbrand', self.test_brand.slug)

    def test_valid_brand_by_many_to_many_field_in_promo(self):
        self.assertEqual('testPromoAction',
                         self.test_brand.from_brand.all()[0].promo_title)


class GoodModelTest(SettingsTestCases):
    """Test model GoodsDB"""

    def test_validators_meta(self):
        print('----------test model GoodsDB----------')
        print(self.test_good._meta.get_field('title').verbose_name, '=',
              self.test_good.title)
        print(self.test_good._meta.get_field('brand').verbose_name, '=',
              self.test_good.brand)
        print(self.test_good._meta.get_field('price').verbose_name, '=',
              self.test_good.price)
        print(self.test_good._meta.get_field('presence').verbose_name, '=',
              self.test_good.presence)
        print(self.test_good._meta.get_field('category').verbose_name, '=',
              self.test_good.category)
        print(self.test_good._meta.get_field('description').verbose_name, '=',
              self.test_good.description)
        print(self.test_good._meta.get_field('date_at').verbose_name, '=',
              self.test_good.date_at)
        print(self.test_good._meta.get_field('slug').verbose_name, '=',
              self.test_good.slug)

    def test_valid_brand(self):
        self.assertEqual('testBrand', self.test_good.brand.title)

    def test_valid_price(self):
        self.assertEqual(Decimal('200.50'), self.test_good.price)

    def test_valid_presence(self):
        self.assertEqual(True, self.test_good.presence)

    def test_valid_category(self):
        self.assertEqual('testCategory', self.test_good.category.title)

    def test_valid_description(self):
        self.assertEqual('TestDescription TestDescription TestDescription',
                         self.test_good.description)

    def test_valid_date_at(self):
        self.assertEqual(self.test_date, self.test_good.date_at.date())

    def test_valid_slug(self):
        self.assertEqual('testgood', self.test_good.slug)


class GalleryModelTest(SettingsTestCases):
    """Test model GalleryDB"""

    def test_validators_meta(self):
        print('----------test model GalleryDB----------')
        print('-------test image №1-------')
        print(self.test_photo_01._meta.get_field('photo').verbose_name, '=',
              self.test_photo_01.photo.url)
        print(self.test_photo_01._meta.get_field('product').verbose_name, '=',
              self.test_photo_01.product)
        print(self.test_photo_01._meta.get_field('slug').verbose_name, '=',
              self.test_photo_01.slug)
        print('-------test image №2-------')
        print(self.test_photo_02._meta.get_field('photo').verbose_name, '=',
              self.test_photo_02.photo.url)
        print(self.test_photo_02._meta.get_field('product').verbose_name, '=',
              self.test_photo_02.product)
        print(self.test_photo_02._meta.get_field('slug').verbose_name, '=',
              self.test_photo_02.slug)

    def test_valid_photo_01_photo(self):
        self.assertEqual(self.test_image_good_01, self.test_photo_01.photo)

    def test_valid_photo_01_photo_url(self):
        self.assertEqual('/media' + self.test_image_good_01,
                         self.test_photo_01.photo.url)

    def test_valid_product_by_photo_01(self):
        self.assertEqual('testGood', self.test_photo_01.product.title)

    def test_valid_photo_02_photo(self):
        self.assertEqual(self.test_image_good_02, self.test_photo_02.photo)

    def test_valid_photo_02_photo_url(self):
        self.assertEqual('/media' + self.test_image_good_02,
                         self.test_photo_02.photo.url)

    def test_valid_product_by_photo_02(self):
        self.assertEqual('testGood', self.test_photo_02.product.title)


class ReviewsModelTest(SettingsTestCases):
    """Test model ReviewsDB"""

    def test_validators_meta(self):
        print('----------test model ReviewsDB----------')
        print('-------test review №1-------')
        print(self.test_review_01._meta.get_field('review_title').verbose_name,
              '=',
              self.test_review_01.review_title)
        print(self.test_review_01._meta.get_field('user_name').verbose_name,
              '=',
              self.test_review_01.user_name)
        print(self.test_review_01._meta.get_field('review_text').verbose_name,
              '=',
              self.test_review_01.review_text)
        print(
            self.test_review_01._meta.get_field('date_at_review').verbose_name,
            '=',
            self.test_review_01.date_at_review)
        print(self.test_review_01._meta.get_field('good').verbose_name, '=',
              self.test_review_01.good)
        print(
            self.test_review_01._meta.get_field('review_rating').verbose_name,
            '=',
            self.test_review_01.review_rating)
        print(self.test_review_01._meta.get_field('slug').verbose_name, '=',
              self.test_review_01.slug)
        print('-------test review №2-------')
        print(self.test_review_02._meta.get_field('review_title').verbose_name,
              '=',
              self.test_review_02.review_title)
        print(self.test_review_02._meta.get_field('user_name').verbose_name,
              '=',
              self.test_review_02.user_name)
        print(self.test_review_02._meta.get_field('review_text').verbose_name,
              '=',
              self.test_review_02.review_text)
        print(
            self.test_review_02._meta.get_field('date_at_review').verbose_name,
            '=',
            self.test_review_02.date_at_review)
        print(self.test_review_02._meta.get_field('good').verbose_name, '=',
              self.test_review_02.good)
        print(
            self.test_review_02._meta.get_field('review_rating').verbose_name,
            '=',
            self.test_review_02.review_rating)
        print(self.test_review_02._meta.get_field('slug').verbose_name, '=',
              self.test_review_02.slug)

    def test_valid_user_by_review_01(self):
        self.assertEqual('testUser', self.test_review_01.user_name.username)

    def test_valid_review_text_by_review_01(self):
        self.assertEqual('ReviewText01 ReviewText01 ReviewText01',
                         self.test_review_01.review_text)

    def test_valid_date_at_by_review_01(self):
        self.assertEqual(self.test_date,
                         self.test_review_01.date_at_review.date())

    def test_valid_good_by_review_01(self):
        self.assertEqual('testGood', self.test_review_01.good.title)

    def test_valid_review_rating_by_review_01(self):
        self.assertEqual('20', self.test_review_01.review_rating)

    def test_valid_slug_by_review_01(self):
        self.assertEqual('review-title-01', self.test_review_01.slug)

    def test_valid_user_by_review_02(self):
        self.assertEqual('testUser', self.test_review_02.user_name.username)

    def test_valid_review_text_by_review_02(self):
        self.assertEqual('ReviewText02 ReviewText02 ReviewText02',
                         self.test_review_02.review_text)

    def test_valid_date_at_by_review_02(self):
        self.assertEqual(self.test_date,
                         self.test_review_02.date_at_review.date())

    def test_valid_good_by_review_02(self):
        self.assertEqual('testGood', self.test_review_02.good.title)

    def test_valid_review_rating_by_review_02(self):
        self.assertEqual('80', self.test_review_02.review_rating)

    def test_valid_slug_by_review_02(self):
        self.assertEqual('review-title-02', self.test_review_02.slug)
