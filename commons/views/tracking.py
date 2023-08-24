from django.shortcuts import render, redirect, get_object_or_404

from commons.const import STEPS
from commons.models.sale import Sale
from commons.tasks.sale import next_step


def enter_purchase_code(request):
    """
    Allows a user to enter a purchase code and be redirected to view its steps.

    If the request method is POST, this view will try to find the sale with the provided code.
    If the sale is found, the user will be redirected to its steps view.
    Otherwise, they will see the form to enter the purchase code again.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered HTML response for entering the purchase code or a redirect to the purchase steps view.
    """
    if request.method == 'POST':
        code = request.POST.get('code')
        if not Sale.objects.filter(code=code).exists():
            return render(request, 'error.html',
                          {'message': 'Codígo de rastreo não encontrado, verifique se o codígo está correto'})

        sale = Sale.objects.get(code=code)
        return redirect('view_purchase_steps', sale_id=sale.id)
    return render(request, 'enter_purchase_code.html')


def view_purchase_steps(request, sale_id):
    """
    Display the steps (trackings) associated with a given sale.

    This view fetches the sale by its ID and then retrieves all trackings related to this sale.
    It then passes these trackings to the template for rendering.

    Args:
        request (HttpRequest): The request object.
        sale_id (int): The ID of the sale whose steps are to be viewed.

    Returns:
        HttpResponse: Rendered HTML response showing the purchase steps for the given sale.
    """
    sale = get_object_or_404(Sale, id=sale_id)
    next_step(sale)
    trackings = sale.sale_tracking.all()
    print(len(trackings), len(STEPS))
    context = {'trackings': trackings, 'sale': sale, 'progress_percentage': (len(trackings) / len(STEPS))*100}
    return render(request, 'view_purchase_steps.html', context)
