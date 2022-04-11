from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.safestring import mark_safe

from .models import PromotionDB, PromotionPhotoDB


class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None,
         {'fields': ('url', 'title', 'content', 'sites', 'template_name',
                     'registration_required')
          }
         ),
    )
    save_on_top = True


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


class PromotionPhotoInLine(admin.TabularInline):
    fk_name = 'promotion'
    model = PromotionPhotoDB


@admin.register(PromotionDB)
class PromotionAdmin(admin.ModelAdmin):
    inlines = (PromotionPhotoInLine, )
    list_display = ('promo_title', 'is_active', 'category_name', 'brand_name',
                    'discount', 'slug',)
    list_filter = ('is_active', 'category',  'brand', 'discount',)
    list_editable = ('is_active', )
    search_fields = ('promo_title', 'category_name', 'brand_name',)
    # fieldsets = (
    #     ('Акция', {
    #         'fields': (
    #             ('promo_title', 'is_active'),
    #             ('category', 'category_name'),
    #             ('brand', 'brand_name'),
    #             'discount',
    #             'description',)
    #     })
    # )

    save_on_top = True
    save_as = True


@admin.register(PromotionPhotoDB)
class PromotionPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'slug', 'get_photo', 'promotion',)
    list_display_links = ('photo', 'slug',)
    readonly_fields = ('get_photo', 'slug',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')
        return 'Фото отсутствует'

    get_photo.short_description = 'Фото акции'
