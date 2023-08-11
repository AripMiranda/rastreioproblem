from django.shortcuts import render
from django.utils import timezone

from commons.models.shop import Shop


def homepage(request):
    premium_shops = Shop.objects.filter(premium_expiration_date__gt=timezone.now())[:5]
    
    return render(request, 'homepage.html', {'premium_shops': premium_shops})
