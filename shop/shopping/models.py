from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from  django.contrib.auth.models import User


class BrandNameDB(models.Model):
    '''list of manufacturers of goods'''
    title = models.CharField(max_length=250, verbose_name='Производитель')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL производителя')

    def get_absolute_url(self):
        return reverse('brand', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Производитель(я)'
        verbose_name_plural = 'Производители(ей)'
        ordering = ('title',)


class CategoryDB(MPTTModel):
    '''The model of category.'''
    title = models.CharField(max_length=100, unique=True, verbose_name='Категория', )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_category',
                            verbose_name='Назначьте родительскую категорию', )
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True, verbose_name='Фото',)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL категории', )

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.title)

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории(ий)'
        ordering = ('title',)
        # index_together = ('pk', 'slug',)


class ReviewsDB(models.Model):
    '''Model of Reviews for godds'''
    UGLI = '1'
    NO_GOOD = '2'
    NORMAL = '3'
    GOOD = '4'
    GREAT = '5'
    RATINGS_CHOICES = (
        (UGLI, 'Ужасно'),
        (NO_GOOD, 'Плохо'),
        (NORMAL, 'Нормально'),
        (GOOD, 'Хорошо'),
        (GREAT, 'Отлично'),
    )
    title = models.CharField(max_length=150, verbose_name='Название отзыва')
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='review_user_name', verbose_name='Имя пользователя')
    description = models.TextField(blank=True, verbose_name='Текст отзыва')
    date_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания отзыва')
    good = models.ForeignKey('GoodsDB', on_delete=models.CASCADE, related_name='review_for_good', null=True,
                             verbose_name='К какому товару привязан отзыв')
    rating = models.CharField(max_length=1, choices=RATINGS_CHOICES, default=NORMAL, verbose_name='Рейтинг товара')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL отзыва')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Отзыв(а)'
        verbose_name_plural = 'Отзывы(ов)'
        ordering = ('-date_at',)


class GalleryDB(models.Model):
    '''Gallery of images by product'''
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото',)
    product = models.ForeignKey('GoodsDB', on_delete=models.CASCADE, related_name='images_for_goods', null=True,
                                verbose_name='Картинка привязана к товару',)
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL картинки',)

    def get_absolute_url(self):
        return reverse('show_image', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.photo)

    class Meta:
        verbose_name = 'Картинка(у)'
        verbose_name_plural = 'Картинки(ок)'
        # ordering = ('photo',)


class GoodsDB(models.Model):
    '''Model of goods'''
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    brand = models.ForeignKey(BrandNameDB, on_delete=models.PROTECT, related_name='brand_good',
                              verbose_name='Производитель')
    price = models.IntegerField(default=0, verbose_name='Цена товара')
    presence = models.BooleanField(default=True, verbose_name='Наличие в магазине')
    category = TreeForeignKey(CategoryDB, on_delete=models.PROTECT, related_name='category_good',
                              verbose_name='Категория товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    date_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    n_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL товара')

    def get_absolute_url(self):
        return reverse('good', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Товар(а)'
        verbose_name_plural = 'Товары(ов)'
        ordering = ('-date_at',)
