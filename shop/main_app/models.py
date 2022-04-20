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

    # TODO валидация если категории - нет, бренда - нет
    # def clean_fields(self, exclude=None):
    #     super().clean_fields(exclude=exclude)
    #     errors = {}
    #
    #     if not self.category and not self.brand:
    #         errors['category'] = ValidationError(
    #                 'Не указана категория, участвующая в акции'
    #         )
    #         errors['brand'] = ValidationError(
    #                 'Не указан производитель, участвующий в акции'
    #         )
    #
    #     if errors:
    #         raise ValidationError(errors)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ('-is_active', )
