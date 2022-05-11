from django.core import validators
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField
from uuslug import uuslug

from shopping.models import BrandNameDB, CategoryDB


def instance_slug(instance):
    return instance.title


def slugify_value(value):
    return value.replace(' ', '-')


class PromotionDB(models.Model):
    """
    Model PromotionDB to save new promotions to database
    """

    promo_title = models.CharField(
            max_length=30,
            verbose_name='Название акции'
    )
    is_active = models.BooleanField(
            default=False,
            verbose_name='Активна'
    )
    category = models.ManyToManyField(
            CategoryDB,
            related_name='from_category',
            blank=True,
            verbose_name='Категория'
    )
    brand = models.ManyToManyField(
            BrandNameDB,
            related_name='from_brand',
            blank=True,
            verbose_name='Производитель'
    )
    discount = models.DecimalField(
            max_digits=3,
            decimal_places=2,
            verbose_name='Скидка',
            null=True,
            help_text='От 0.01 до 0.99',
            validators=[
                validators.MinValueValidator(0.01),
                validators.MaxValueValidator(0.99)
            ]
    )
    description = models.TextField(
            blank=True,
            verbose_name='Описание акции'
    )
    photo = models.ImageField(
            upload_to='photo/promo/%Y/%m/%d',
            verbose_name='Фото',
            null=True
    )
    slug = AutoSlugField(
            max_length=35,
            db_index=True,
            unique=True,
            verbose_name='URL Акции',
            populate_from=instance_slug,
            slugify=slugify_value
    )

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.promo_title, instance=self)
        super(PromotionDB, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('promo', kwargs={'slug_promo': self.slug})

    def __str__(self):
        return f'{self.promo_title}'

    def get_category(self):
        return ','.join([str(category) for category in self.category.all()])

    def get_brand(self):
        return ','.join([str(brand) for brand in self.brand.all()])

    class Meta:
        verbose_name = 'Акция(ю)'
        verbose_name_plural = 'Акции(ий)'
        ordering = ('-is_active',)
