from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import CategoryDB, BrandNameDB, GalleryDB, ReviewsDB, GoodsDB

# python manage.py test
User = get_user_model()

class ShoppingTestCases(TestCase):

    def setUp(self) -> None:    # предварительные настройки
        user = User.objects.create(username='testUser', password='password')
        self.test_category_parent = CategoryDB.objects.create(title='TestCategoryParent')
        self.test_category_child = CategoryDB.objects.create(title='TestCategoryChild',
                                                             parent=self.test_category_parent)
        self.test_brand = BrandNameDB.objects.create(title='TestBrand')
        # self.test_good_01 = GoodsDB.objects.create(
        #
        # )

        image_01 = SimpleUploadedFile("test_image_01.jpg", content=b'', content_type="test_image_01/jpg")
        image_02 = SimpleUploadedFile("test_image_02.jpg", content=b'', content_type="test_image_02/jpg")
        # self.test_review_01 = ReviewsDB.objects.create()
        # self.test_review_02 = ReviewsDB.objects.create()
        # self.test_image_01 = GalleryDB.objects.create()
        # self.test_image_02 = GalleryDB.objects.create()
