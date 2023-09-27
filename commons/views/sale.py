from django.contrib import messages
from django.shortcuts import render, redirect

from commons.const import PRICE_BY_TRACKING, available_steps
from commons.models.profile import Profile
from commons.models.sale import Sale
from commons.models.shop import Shop
from commons.models.tracking import Tracking
from commons.tasks.email import send_email


def list_orders(request, profile_id):
    referral_code = request.GET.get('referral')
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return render(request, 'error.html', {'message': 'CPF não encontrado!'})

    orders = Sale.objects.filter(profile=profile)

    return render(request, 'list_orders.html', {'profile': profile, 'orders': orders, 'referral': referral_code})


def generate_sale_by_store(request, store_id):
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


def create_order(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return redirect('create_sale')
    referral_code = request.GET.get('referral')

    shop = Shop.objects.get(referral=referral_code)

    if shop.points_balance < PRICE_BY_TRACKING:
        messages.error(request, 'A loja não tem pontos suficientes para autorizar a venda.')
        send_email([Shop.email],
                   {'subject': 'Notificação de Saldo de pontos',
                    'message': f'Uma solicitação de rasteio foi feita, mas a loja não possui pontos o suficiente para '
                               f'concluir, favor entra em contato com administração do site.'})

        return render(request, 'error.html',
                      {'message': 'Erro inesperado, favor entrar em contato com administração da loja.',
                       'contact': shop.email})
    else:
        sale = Sale.objects.create(shop=shop, profile=profile)
        shop.points_balance -= PRICE_BY_TRACKING
        shop.save()
        sale.save()
        tracking = Tracking.objects.create(sale=sale, description=available_steps[0])
        tracking.save()

        messages.success(request, 'Venda criada com sucesso!')

    return redirect(redirect('list_orders', profile_id=profile.id).url + f'?referral={referral_code}')
