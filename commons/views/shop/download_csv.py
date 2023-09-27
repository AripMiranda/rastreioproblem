import csv

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from commons.models.sale import Sale
from commons.models.shop import Shop


def shop_reports(request):
    shop_id = request.session.get('shop_id')
    shop = get_object_or_404(Shop, id=shop_id)

    return render(request, 'shop_reports.html', {'shop': shop})


def generate_csv_report(request, shop_id):
    # Consulte o banco de dados para obter os registros desejados (por exemplo, vendas)
    shop = get_object_or_404(Shop, id=shop_id)

    # Consulte o banco de dados para obter os registros desejados (por exemplo, vendas do shop_id)
    sales = Sale.objects.filter(shop=shop)

    # Crie uma resposta HTTP com o tipo de conteúdo apropriado para CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_de_vendas.csv"'

    # Crie um objeto de escrita CSV
    writer = csv.writer(response)

    # Escreva os cabeçalhos no arquivo CSV (nomes das colunas)
    writer.writerow(['ID da Venda', 'Descrição', 'Valor', 'Data da Venda', 'Código', 'Finalizada'])

    # Escreva os dados das vendas no arquivo CSV
    for sale in sales:
        writer.writerow([sale.id, sale.description, sale.value, sale.sale_date, sale.code, sale.finished])

    return response
