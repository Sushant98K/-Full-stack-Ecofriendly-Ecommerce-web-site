from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product  # Replace with your actual product model import
from .models import Order

@login_required
def order_now(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            # Redirect to order form page
            return render(request, 'orders/order_form.html', {'product': product})
    return redirect('product_list')

@login_required
def order_submit(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        product = get_object_or_404(Product, id=product_id)
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            address=address,
            phone=phone
        )

        messages.success(request, f"Order placed successfully for {product.name}.")
        return redirect('product_list')
    return redirect('product_list')

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by("-order_date")
    return render(request, "orders/my_orders.html", {"orders": orders})