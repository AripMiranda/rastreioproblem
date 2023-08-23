from django.shortcuts import render, redirect

from commons.models.profile import Profile
from commons.models.shop import Shop


def consult_cpf(request):
    referral_code = request.GET.get('referral')

    if not referral_code:
        return render(request, 'request_store_code.html')

    try:
        shop = Shop.objects.get(referral=referral_code)
    except Shop.DoesNotExist:
        return render(request, 'error.html', {'message': 'Loja não encontrada!'})

    cpf = request.POST.get('cpf')

    if not cpf:
        return render(request, 'request_cpf.html', {'referral': referral_code})

    try:
        profile = Profile.objects.get(cpf=cpf)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(cpf=cpf)

    return redirect(redirect('list_orders', profile_id=profile.id).url + f'?referral={referral_code}')
