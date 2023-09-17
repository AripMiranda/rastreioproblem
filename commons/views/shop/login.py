from django.shortcuts import render, redirect

from commons.models.shop import Shop


def shop_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = Shop.authenticate(request, email=email, password=password)

        if user is not None:
            request.session['shop_id'] = user.id
            return redirect('shop_reports')
        else:
            error_message = 'Credenciais inválidas. Tente novamente.'
            return render(request, 'shop_login.html', {'error_message': error_message})

    return render(request, 'shop_login.html')
