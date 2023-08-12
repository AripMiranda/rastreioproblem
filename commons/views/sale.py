from django.contrib import messages
from django.shortcuts import render, redirect

from commons.const import PRICE_BY_TRACKING
from commons.models.sale import Sale
from commons.models.shop import Shop


def create_sale(request):
    """
    Render the store details based on the referral code passed in the request.

    If no referral code is provided, prompt the user to input it.
    If a store with the provided referral code does not exist, display an error.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered HTML response for store details, request for store code or error page.
    """
    referral = request.GET.get('referral')
    if not referral:
        return render(request, 'request_store_code.html')

    try:
        shop = Shop.objects.get(referral=referral)
    except shop.DoesNotExist:
        return render(request, 'error.html', {'message': 'Loja não encontrada!'})
    sales_count = Sale.objects.filter(shop=shop).count()
    return render(request, 'store_details.html', {'store': shop, 'sales_count': sales_count})


def generate_sale(request, store_id):
    """
    Generate a sale for a specified store.

    If the store has insufficient points for the sale, display an error.
    If the store has sufficient points, deduct the points, create the sale and redirect to the purchase steps view.

    Args:
        request (HttpRequest): The request object.
        store_id (int): The ID of the store for which the sale is to be generated.

    Returns:
        HttpResponse: Redirect to the purchase steps view or store creation view or an error page.
    """
    try:
        shop = Shop.objects.get(pk=store_id)
    except shop.DoesNotExist:
        return render(request, 'error.html', {'message': 'Loja não encontrada!'})

    if shop.points_balance < PRICE_BY_TRACKING:
        messages.error(request, 'A loja não tem pontos suficientes para autorizar a venda.')
        return render(request, 'error.html', {'message': 'A loja não tem pontos suficientes para autorizar a venda!'})
    else:
        sale = Sale.objects.create(shop=shop)
        shop.points_balance -= PRICE_BY_TRACKING
        shop.save()
        sale.save()
        messages.success(request, 'Venda criada com sucesso!')
        return redirect('view_purchase_steps', sale_id=sale.id)
