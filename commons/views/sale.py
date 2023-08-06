from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from commons.const import PRICE_BY_TRACKING
from commons.forms.sale import SaleForm
from commons.models.shop import Shop


def create_sale(request, referral):
    shop = get_object_or_404(Shop, referral=referral)

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.shop = shop

            if shop.points_balance < PRICE_BY_TRACKING:
                messages.error(request, 'A loja não tem pontos suficientes para autorizar a venda.')
            else:
                shop.points_balance -= PRICE_BY_TRACKING
                shop.save()
                sale.save()
                messages.success(request, 'Venda criada com sucesso!')
                return redirect('view_purchase_steps', sale_id=sale.id)

    else:
        form = SaleForm()

    context = {'form': form, 'shop': shop}
    return render(request, 'create_sale.html', context)
