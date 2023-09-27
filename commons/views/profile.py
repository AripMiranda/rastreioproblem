from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from commons.forms.profile import ProfileCreationForm
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

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        if email is None:
            try:
                profile = Profile.objects.get(cpf=cpf)
                return redirect(redirect('list_orders', profile_id=profile.id).url + f'?referral={referral_code}')
            except Profile.DoesNotExist:
                return render(request, 'request_email.html', {'referral': referral_code})

        form = ProfileCreationForm(request.POST)

        if form.is_valid():
            profile = form.save()
            return redirect(redirect('list_orders', profile_id=profile.id).url + f'?referral={referral_code}')
    else:
        form = ProfileCreationForm()

    return render(request, 'request_cpf.html', {'referral': referral_code, 'form': form})
