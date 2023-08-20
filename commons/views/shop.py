from django.shortcuts import render, get_object_or_404
from commons.models.shop import Shop  # Importe o modelo da loja


def shop_details(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)  # Obtém a instância da loja ou retorna 404
    return render(request, 'shop_details.html', {'shop': shop})  # Renderiza o template com os detalhes da loja
