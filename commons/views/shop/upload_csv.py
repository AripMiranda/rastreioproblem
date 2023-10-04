from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
import pandas as pd
from io import StringIO
from validate_docbr import CPF
from commons.forms.upload import UploadCSVForm
from commons.models.profile import Profile
from commons.models.sale import Sale
from commons.models.shop import Shop


def upload_csv(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_file))
            response_data = []

            if 'CPF' not in df.columns and 'cpf' not in df.columns:
                return render(request, 'error.html', {'message': 'A coluna CPF não está presente no CSV.'})

            total_rows = len(df.index)
            if shop.points_balance < total_rows:
                return render(request, 'error.html', {'message': 'Saldo insuficiente na loja.'})

            cpf_validator = CPF()
            for index, row in df.iterrows():
                cpf = str(row['CPF'])

                if not cpf_validator.validate(cpf):
                    return render(request, 'error.html', {'message': f'CPF inválido: {cpf}'})

                email = row.get('Email', None)
                profile, created = Profile.objects.get_or_create(cpf=cpf,
                                                                 defaults={'email': email if pd.notna(email) else ''})

                if email and pd.notna(email) and not profile.email:
                    profile.email = email
                    profile.save()

                sale = Sale.objects.create(shop=shop, profile=profile, value=0)
                response_data.append([cpf, email if pd.notna(email) else '', sale.code])

            shop.points_balance -= total_rows  # Descontando os pontos após o processamento bem-sucedido
            shop.save()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="sales.csv"'

            writer = csv.writer(response)
            writer.writerow(['CPF', 'Email', 'Código'])  # Cabeçalho do CSV
            writer.writerows(response_data)  # Dados do CSV

            return response

    else:
        form = UploadCSVForm()
    return render(request, 'upload.html', {'form': form, 'shop': shop})
