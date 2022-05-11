from django.contrib import admin

from .models import OrderDB, OrderItemDB
from .tasks import send_order_mail


def send_order_mails(modeladmin, request, queryset):
    """
    The function for sending mails to users about orders dispatchment
    """

    for rec in queryset:
        if rec.status != OrderDB.SENT:
            send_order_mail.delay(rec.id, rec.for_user.id)
            rec.status = OrderDB.SENT
            rec.save()
    modeladmin.message_user(request, 'Письма об отправке заказа направлены')


send_order_mails.short_description = 'Заказ отправлен'


class OrderItemInline(admin.TabularInline):
    model = OrderItemDB
    raw_id_fields = ['product']


@admin.register(OrderDB)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_user', 'status', 'date_at', 'date_up',)
    list_display_links = ('id', 'for_user', 'date_at', 'date_up',)
    list_filter = ('status', 'date_at', 'date_up',)
    list_editable = ('status',)
    readonly_fields = ('id', 'date_at', 'date_up', 'get_full_name')
    inlines = (OrderItemInline,)
    actions = (send_order_mails,)
    save_on_top = True
    fieldsets = (
        ('О заказе', {
            'fields': ('id', 'status', 'date_at', 'date_up', 'delivery_type')
        }),
        ('Покупатель', {
            'fields': ('for_user', 'get_full_name')
        }),
        ('Адрес доставки', {
            'fields': ('postal_code', 'country', 'region', 'city', 'address',
                       'phone_number',)
        }),
    )

    def get_full_name(self, obj):
        return obj.for_user.get_full_name()

    get_full_name.short_description = 'ФИО покупателя'
