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
from django.contrib import admin
from django.urls import path
from commons.views.home import homepage

from commons.views.sale import create_sale, generate_sale
from commons.views.tracking import enter_purchase_code, view_purchase_steps
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name='homepage'), 
    path('admin/', admin.site.urls),
    path('create_sale/', create_sale, name='create_sale'),
    path('generate_sale/<int:store_id>/', generate_sale, name='generate_sale'),
    path('enter_code/', enter_purchase_code, name='enter_purchase_code'),
    path('purchase_steps/<int:sale_id>/', view_purchase_steps, name='view_purchase_steps'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)