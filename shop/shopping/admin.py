from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from .models import GalleryDB, CategoryDB, BrandNameDB, GoodsDB, ReviewsDB


class ReviewInLine(admin.TabularInline):
    fk_name = 'good'
    model = ReviewsDB


class GalleryInLine(admin.TabularInline):
    fk_name = 'product'
    model = GalleryDB


@admin.register(CategoryDB)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug', 'get_photo')
    list_display_links = ('indented_title',)
    readonly_fields = ('get_photo', 'slug',)
    list_per_page = 10

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')
        return 'Фото не установленно'

    get_photo.short_description = 'Миниатюра'


@admin.register(GalleryDB)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('photo', 'get_photo', 'slug', 'product')
    list_display_links = ('photo', 'slug',)
    readonly_fields = ('get_photo', 'slug',)
    list_per_page = 10

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')
        return 'Фото не установленно'

    get_photo.short_description = 'Миниатюра'


@admin.register(ReviewsDB)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('review_title', 'good', 'review_rating', 'slug',
                    'date_at_review', 'user_name',)
    list_display_links = ('review_title', 'slug', 'date_at_review',)
    readonly_fields = ('date_at_review', 'slug',)
    list_editable = ('review_rating', 'user_name',)
    list_per_page = 10


@admin.register(BrandNameDB)
class BrandNameAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title', 'slug',)
    list_per_page = 10


@admin.register(GoodsDB)
class GoodsAdmin(admin.ModelAdmin):
    inlines = (GalleryInLine, ReviewInLine)
    list_display = ('title', 'brand', 'price', 'presence', 'category',
                    'date_at', 'n_views', 'slug',)
    list_display_links = ('title',)
    search_fields = ('title', 'price')
    list_editable = ('presence', 'category',)
    list_filter = ('brand', 'price', 'presence', 'category',)
    readonly_fields = ('date_at', 'n_views', 'slug',)
    list_per_page = 10
    fieldsets = (
        ('О товаре', {
            'fields': ('title', 'brand', 'description',)
        }),
        ('Иная информация', {
            'fields': (
            'price', 'slug', 'category', 'presence', 'date_at', 'n_views',)
        }),
    )
    save_on_top = True
    save_as = True
