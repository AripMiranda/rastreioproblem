from django.contrib import admin

from commons.models.profile import Profile
from commons.models.sale import Sale
from commons.models.shop import Shop
from commons.models.tracking import Tracking


# Register your models here.


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('shop', 'description', 'value', 'sale_date', 'code')
    list_filter = ('shop', 'sale_date')
    search_fields = ('shop__name', 'description', 'code')
    ordering = ('-sale_date',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'points_balance', 'referral', 'custom_referral', 'created_date')
    list_filter = ('name', 'created_date')
    search_fields = ('name', 'email', 'referral')
    readonly_fields = ('password',)

    ordering = ('-created_date',)


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'cpf')
    list_filter = ('email', 'cpf')
    search_fields = ('email', 'cpf')
    ordering = ('-id',)
    pass
