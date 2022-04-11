from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from uuslug import uuslug
from autoslug import AutoSlugField
from django.core import validators

from shopping.models import BrandNameDB, CategoryDB


def instance_slug(instance):
    return instance.title


def slugify_value(value):
    return value.replace(' ', '-')


class PromotionDB(models.Model):
    """doc string"""
    promo_title = models.CharField(
            max_length=30,
            verbose_name='Название акции'
    )
    is_active = models.BooleanField(
            default=False,
            verbose_name='Активна'
    )
    category = models.BooleanField(
            default=False,
            verbose_name='Участие категории'
    )
    category_name = models.ForeignKey(
            CategoryDB,
            on_delete=models.PROTECT,
            related_name='from_category',
            null=True,
            blank=True,
            verbose_name='Категория'
    )
    brand = models.BooleanField(
            default=False,
            verbose_name='Участие производителя'
    )
    brand_name = models.ForeignKey(
            BrandNameDB,
            on_delete=models.PROTECT,
            related_name='from_brand',
            null=True,
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
        return reverse('brand', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.promo_title}'

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        errors = {}

        if self.category and not self.category_name:
            errors['category_name'] = ValidationError(
                    'Не указана категория, участвующая в акции'
            )
        if not self.category and self.category_name:
            errors['category_name'] = ValidationError(
                    'Категории не участвуют в акции'
            )

        if self.brand and not self.brand_name:
            errors['brand_name'] = ValidationError(
                    'Не указан производитель, участвующий в акции'
            )
        if not self.brand and self.brand_name:
            errors['brand_name'] = ValidationError(
                    'Производители не участвуют в акции'
            )

        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ('-is_active', )


class PromotionPhotoDB(models.Model):
    """doc string"""
    photo = models.ImageField(
            upload_to='photo/promo/%Y/%m/%d',
            verbose_name='Фото'
    )
    promotion = models.ForeignKey(
            PromotionDB,
            on_delete=models.CASCADE,
            related_name='images_for_promo',
            verbose_name='Фото привязано к акции'
    )
    slug = AutoSlugField(
            max_length=255,
            db_index=True,
            unique=True,
            verbose_name='URL Фото акции',
            populate_from=instance_slug,
            slugify=slugify_value
    )

    def save(self, *args, **kwargs):
        self.slug = uuslug(str(self.photo), instance=self)
        super(PromotionPhotoDB, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('show_image', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.photo}'

    class Meta:
        verbose_name = 'Фото акции'
        verbose_name_plural = 'Фото акций'




