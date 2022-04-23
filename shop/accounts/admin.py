from django.contrib import admin
import datetime

from .models import ShopUser
from .utilities import send_activation_notification
from shopping.models import ReviewsDB


# TODO inline orders?
def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма для активации отправлены')


send_activation_notifications.short_description = 'Отправка писем для активации'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более трех дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        status = self.value()
        if status == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif status == 'threedays':
            date_not_activated = datetime.date.today() - \
                                 datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined__date__lt=date_not_activated)
        elif status == 'week':
            date_not_activated = datetime.date.today() - \
                                 datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined__date__lt=date_not_activated)


class ReviewInline(admin.TabularInline):
    fk_name = 'user_name'
    model = ReviewsDB


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    inlines = (ReviewInline,)
    list_display = ('__str__', 'email', 'is_activated', 'date_joined',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    list_filter = (NonactivatedFilter,)
    readonly_fields = ('last_login', 'date_joined',)
    actions = (send_activation_notifications,)
    fieldsets = (
        ('Основная информация', {
            'fields': (
                ('username', 'email'),
                ('first_name', 'middle_name', 'last_name'),
                ('is_active', 'is_activated'),
                ('is_staff', 'is_superuser'),
                ('last_login', 'date_joined'),
            )
        }),
        ('Дополнительная информация', {
            'fields': (
                'phone_number', ('postcode', 'country'), 'region', 'city',
                'address'
            )
        })
    )


