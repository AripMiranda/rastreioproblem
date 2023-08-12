PRICE_BY_TRACKING = 100

_steps = [
    "Processando pedido",
    "Objeto Postado",
    "Objeto recebido pelos Correios do Brasil",
    "Fiscalização aduaneira finalizada",
    "Objeto em trânsito - por favor aguarde",
]


def list_to_dict(lst):
    d = {}
    for i in range(1, len(lst)):
        d[lst[i - 1]] = lst[i]
    return d

STEPS = list_to_dict(_steps)
