"""
URL configuration for tracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from commons.views.profile import consult_cpf
from commons.views.sale import generate_sale_by_store, list_orders, create_order
from commons.views.shop.create import create_shop
from commons.views.shop.details import shop_details
from commons.views.shop.download_csv import shop_reports, generate_csv_report
from commons.views.shop.login import shop_login
from commons.views.tracking import enter_purchase_code, view_purchase_steps

urlpatterns = [
    path('', consult_cpf, name='homepage'),
    path('admin/', admin.site.urls),
    path('order/', consult_cpf, name='create_sale'),
    path('new_order/<int:profile_id>/', create_order, name='create_order'),
    path('order_by_store/<int:store_id>/', generate_sale_by_store, name='generate_sale'),
    path('orders/<int:profile_id>/', list_orders, name='list_orders'),
    path('enter_code/', enter_purchase_code, name='enter_purchase_code'),
    path('purchase_steps/<int:sale_id>/', view_purchase_steps, name='view_purchase_steps'),
    path('shop/<int:shop_id>/', shop_details, name='shop_details'),
    path('login/', shop_login, name='shop_login'),
    path('shop_reports/', shop_reports, name='shop_reports'),
    path('generate_csv_report/<int:shop_id>/', generate_csv_report, name='generate_csv_report'),
    path('create_shop/', create_shop, name='shop_create'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
