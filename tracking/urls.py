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

from commons.views.home import homepage
from commons.views.profile import consult_cpf
from commons.views.sale import generate_sale_by_store, list_orders, create_order
from commons.views.shop import shop_details
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
    path('shop/<int:shop_id>/', shop_details, name='shop_details')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
