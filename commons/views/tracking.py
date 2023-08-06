from django.shortcuts import render, redirect, get_object_or_404

from commons.models.sale import Sale


def enter_purchase_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        sale = get_object_or_404(Sale, code=code)
        return redirect('view_purchase_steps', sale_id=sale.id)
    return render(request, 'enter_purchase_code.html')


def view_purchase_steps(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    trackings = sale.sale_tracking.all()
    context = {'trackings': trackings, 'sale': sale}
    return render(request, 'view_purchase_steps.html', context)
