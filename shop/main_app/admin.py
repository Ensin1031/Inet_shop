from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage


from .forms import PromotionForm
from .models import PromotionDB


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


@admin.register(PromotionDB)
class PromotionAdmin(admin.ModelAdmin):
    form = PromotionForm
    list_display = ('__str__', 'is_active', 'get_category', 'get_brand',
                    'discount', 'photo', 'slug',)
    list_filter = ('is_active', 'discount', 'category', 'brand',)
    list_editable = ('is_active',)
    search_fields = ('promo_title', 'category', 'brand',)
    fields = (('promo_title', 'is_active'), 'discount',
              'category', 'brand', 'photo',)
    filter_horizontal = ('category', 'brand',)
    save_on_top = True

    def get_category(self, obj):
        return obj.get_category()

    get_category.short_description = 'Категория'

    def get_brand(self, obj):
        return obj.get_brand()

    get_brand.short_description = 'Производитель'


