from django.contrib import admin

from .models import OrderDB, OrderItemDB


class OrderItemInline(admin.TabularInline):
    model = OrderItemDB
    raw_id_fields = ['product']


@admin.register(OrderDB)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_user', 'status', 'date_at', 'date_up',)
    list_display_links = ('id', 'for_user', 'date_at', 'date_up',)
    list_filter = ('status', 'date_at', 'date_up',)
    list_editable = ('status',)
    readonly_fields = ('id', 'date_at', 'date_up',)
    inlines = (OrderItemInline,)
    fieldsets = (
        ('О заказе', {
            'fields': ('id', 'status', 'date_at', 'date_up', 'delivery_type')
        }),
        ('Покупатель', {
            'fields': ('for_user', 'first_name', 'last_name',)
        }),
        ('Адрес доставки', {
            'fields': ('postal_code', 'country', 'region', 'city', 'address', 'phone_number',)
        }),
    )
    # paginator = 10
    save_on_top = True
