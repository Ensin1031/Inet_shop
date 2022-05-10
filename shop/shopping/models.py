from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from accounts.models import ShopUser
from django.conf import settings
from uuslug import uuslug
from autoslug import AutoSlugField


def instance_slug(instance):
    return instance.title


def slugify_value(value):
    return value.replace(' ', '-')


class BrandNameDB(models.Model):
    """list of manufacturers of goods"""
    title = models.CharField(max_length=250, verbose_name='Производитель')
    slug = AutoSlugField(max_length=250, db_index=True, unique=True, verbose_name='URL Производителя',
                         populate_from=instance_slug, slugify=slugify_value)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(BrandNameDB, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('brand', kwargs={'slug_brand': self.slug})

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Производитель(я)'
        verbose_name_plural = 'Производители(ей)'
        ordering = ('title',)


class CategoryDB(MPTTModel):
    """The model of category."""
    title = models.CharField(max_length=100, unique=True, verbose_name='Категория', )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_category',
                            verbose_name='Назначьте родительскую категорию', )
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True, verbose_name='Фото',)
    slug = AutoSlugField(max_length=100, db_index=True, unique=True, verbose_name='URL Категории',
                         populate_from=instance_slug, slugify=slugify_value)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(CategoryDB, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug_cat': self.slug})

    def __str__(self):
        return str(self.title)

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории(ий)'
        ordering = ('title',)


class ReviewsDB(models.Model):
    """Model of Reviews for goods"""
    UGLI = '20'
    NO_GOOD = '40'
    NORMAL = '60'
    GOOD = '80'
    GREAT = '100'
    RATINGS_CHOICES = (
        (UGLI, 'Ужасно'),
        (NO_GOOD, 'Плохо'),
        (NORMAL, 'Нормально'),
        (GOOD, 'Хорошо'),
        (GREAT, 'Отлично'),
    )
    review_title = models.CharField(max_length=150, verbose_name='Название отзыва')
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='review_user_name', verbose_name='Имя пользователя')
    review_text = models.TextField(max_length=500, blank=True, verbose_name='Текст отзыва',)
    date_at_review = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания отзыва')
    good = models.ForeignKey('GoodsDB', on_delete=models.CASCADE, related_name='review_for_good', null=True,
                             verbose_name='К какому товару привязан отзыв')
    review_rating = models.CharField(max_length=3, choices=RATINGS_CHOICES, default=NORMAL, verbose_name='Рейтинг товара')
    slug = AutoSlugField(max_length=150, db_index=True, unique=True, verbose_name='URL Отзыва',
                         populate_from=instance_slug, slugify=slugify_value)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.review_title, instance=self)
        super(ReviewsDB, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('good', kwargs={'slug': self.good.slug})

    def __str__(self):
        return str(self.review_title)

    class Meta:
        verbose_name = 'Отзыв(а)'
        verbose_name_plural = 'Отзывы(ов)'
        ordering = ('-date_at_review',)


class GalleryDB(models.Model):
    '''Gallery of images by product'''
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото',)
    product = models.ForeignKey('GoodsDB', on_delete=models.CASCADE, related_name='images_for_goods', null=True,
                                verbose_name='Картинка привязана к товару',)
    slug = AutoSlugField(max_length=255, db_index=True, unique=True, verbose_name='URL Картинки',
                         populate_from=instance_slug, slugify=slugify_value)

    def save(self, *args, **kwargs):
        self.slug = uuslug(str(self.photo), instance=self)
        super(GalleryDB, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.photo)

    class Meta:
        verbose_name = 'Картинка(у)'
        verbose_name_plural = 'Картинки(ок)'


class GoodsDB(models.Model):
    """Model of goods"""
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    brand = models.ForeignKey(BrandNameDB, on_delete=models.PROTECT, related_name='brand_good',
                              verbose_name='Производитель')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена товара')
    presence = models.BooleanField(default=True, verbose_name='Наличие в магазине')
    category = TreeForeignKey(CategoryDB, on_delete=models.PROTECT, related_name='category_good',
                              verbose_name='Категория товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    date_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    n_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    slug = AutoSlugField(max_length=255, db_index=True, unique=True, verbose_name='URL Товара',
                         populate_from=instance_slug, slugify=slugify_value)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(GoodsDB, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('good', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Товар(а)'
        verbose_name_plural = 'Товары(ов)'
        ordering = ('-date_at',)
