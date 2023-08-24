PRICE_BY_TRACKING = 100

available_steps = [
    "Pedido sendo separado.",
    "Pedido coletado.",
    "Pedido em transporte",
    "Pedido a caminho do cliente.",
    "Pedido na cidade do destino.",
    "Pedido na rota de entrega"
]


def list_to_dict(lst):
    d = {}
    for i in range(1, len(lst)):
        d[lst[i - 1]] = lst[i]
    return d


STEPS = list_to_dict(available_steps)
