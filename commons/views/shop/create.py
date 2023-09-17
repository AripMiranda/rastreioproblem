from django.shortcuts import render, redirect

from commons.forms.shop import ShopForm


def create_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            new_shop = form.save()

            return redirect('shop_login')
    else:
        form = ShopForm()

    return render(request, 'create_shop.html', {'form': form})
