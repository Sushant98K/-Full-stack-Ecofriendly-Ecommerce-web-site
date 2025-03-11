from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Cart
from django.conf import settings
import razorpay
from django.http import JsonResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from the form, default to 1

    # Check if the item already exists in the cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if created:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect("cart:cart_detail")

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, "cart/cart_detail.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect("cart:cart_detail")

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate total price and convert Decimal to float
    total_price = sum([item.get_total_price() for item in cart_items])  # Assuming get_total_price() returns a Decimal value
    total_price = float(total_price)  # Convert Decimal to float

    # Convert total price to paise
    total_price_in_paise = int(total_price * 100)

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create a Razorpay order
    razorpay_order = client.order.create(dict(
        amount=total_price_in_paise,  # Razorpay expects the amount in paise
        currency='INR',
        payment_capture='1'  # Auto capture payment after success
    ))

    # Save Razorpay order ID in session
    request.session['razorpay_order_id'] = razorpay_order['id']
    request.session['amount'] = total_price

    # Render the checkout page with the Razorpay order ID
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_price_in_paise': total_price_in_paise,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_order': razorpay_order
    }
    return render(request, 'cart/place_order.html', context)

@login_required
@csrf_exempt  # This is required for Razorpay to send POST requests
def payment_success(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        # Retrieve the order ID and secret key from the session
        order_id = request.session.get('razorpay_order_id')
        amount = request.session.get('amount')

        if razorpay_order_id and razorpay_payment_id and razorpay_signature:
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Verify the payment signature
            params = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            # Check whether the signature is valid
            try:
                client.payment.verify_payment_signature(params)
                # Payment is successful, now update the order status or create an order record
                # For example, you can create an Order object in your database here.

                # Here you can save the order details, payment status, etc.
                # For demonstration, let's assume the payment is successful.
                
                # Clear session data related to Razorpay
                del request.session['razorpay_order_id']
                del request.session['amount']

                return JsonResponse({'status': 'success', 'message': 'Payment verified successfully'})

            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({'status': 'error', 'message': 'Payment verification failed'})
        else:
            return redirect('product_list')
        



