import shutil
import tempfile
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.test import TestCase

from accounts.models import ShopUser
from main_app.models import PromotionDB
from shopping.models import CategoryDB, BrandNameDB, GalleryDB, ReviewsDB, GoodsDB
from shopping.get_func import ShowObjects, ShowOneObject, get_promo


# python manage.py test


class SettingsTestCases(TestCase):
    """Parent setting class for all tests by project"""

    @classmethod
    def setUpClass(cls):
        super(SettingsTestCases, cls).setUpClass()
        # получаем дату на данный момент
        cls.test_date = datetime.today().date()
        # папка для временных тестовых медиа-файлов, на момент теста медиа папка будет переопределена
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        # временные картинки для тестов
        cls.test_image_promo = tempfile.NamedTemporaryFile(suffix='.jpg').name
        cls.test_image_good_01 = tempfile.NamedTemporaryFile(suffix='.jpg').name
        cls.test_image_good_02 = tempfile.NamedTemporaryFile(suffix='.jpg').name
        # БД: тестовый юзер
        cls.test_user = ShopUser.objects.create(
            username='testUser',
            first_name='TestFirstName',
            last_name='TestLastName',
            password='testPassword',
            email='testemail@mail.ru',
        )
        # БД: тестовая категория
        cls.test_category_parent = CategoryDB.objects.create(title='testCategoryParent')
        cls.test_category = CategoryDB.objects.create(title='testCategory', parent=cls.test_category_parent)
        # БД: тестовый производитель
        cls.test_brand = BrandNameDB.objects.create(title='testBrand')
        # БД: тестовая промо-акция
        cls.test_promo = PromotionDB.objects.create(
            promo_title='testPromoAction',
            discount=Decimal('0.15'),
            description='TestPromoDescription TestPromoDescription TestPromoDescription',
            photo=cls.test_image_promo,
        )
        cls.test_promo.category.add(cls.test_category)
        cls.test_promo.brand.add(cls.test_brand)
        # БД: тестовый товар
        cls.test_good = GoodsDB.objects.create(
            title='testGood',
            brand=cls.test_brand,
            category=cls.test_category,
            price=Decimal('200.50'),
            description='TestDescription TestDescription TestDescription',
        )
        # БД: тестовые картинки, привязаные к тестовому товару
        cls.test_photo_01 = GalleryDB.objects.create(
            photo=cls.test_image_good_01,
            product=cls.test_good,
        )
        cls.test_photo_02 = GalleryDB.objects.create(
            photo=cls.test_image_good_02,
            product=cls.test_good,
        )
        # БД: тестовые отзывы к тестовому товару, написаные тестовым пользователем)
        cls.test_review_01 = ReviewsDB.objects.create(
            review_title='review_title_01',
            user_name=cls.test_user,
            review_text='ReviewText01 ReviewText01 ReviewText01',
            good=cls.test_good,
            review_rating='20',
        )
        cls.test_review_02 = ReviewsDB.objects.create(
            review_title='review_title_02',
            user_name=cls.test_user,
            review_text='ReviewText02 ReviewText02 ReviewText02',
            good=cls.test_good,
            review_rating='80',
        )

    @classmethod
    def tearDownClass(cls):
        super(SettingsTestCases, cls).tearDownClass()
        # рекурсивно удаляем временную папку после завершения тестов
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


class ForGetFuncTests(SettingsTestCases):
    """set objects for testing class ShowObjects in shopping.get_func"""
    def setUp(self) -> None:
        self.test_category_fgf = CategoryDB.objects.create(title='testCategoryFGF', parent=self.test_category_parent)
        self.test_promo_fgf = PromotionDB.objects.create(
            promo_title='testPromoActionFGF',
            discount=Decimal('0.25'),
            description='TestPromoDescriptionFGF',
            photo=self.test_image_promo,
            is_active=True,
        )
        self.test_promo_fgf.category.add(self.test_category_fgf)
        self.test_good_for_get_func = GoodsDB.objects.create(
            title='testGoodForGetFunc',
            brand=self.test_brand,
            category=self.test_category_fgf,
            price=Decimal('200.50'),
            description='TestDescription TestDescription TestDescription',
            n_views=5,
        )
        self.test_list = ShowObjects(GoodsDB.objects.filter(title__contains='test'))
        self.test_object = ShowOneObject(self.test_good)
        self.test_get_promo = get_promo(self.test_good_for_get_func)
