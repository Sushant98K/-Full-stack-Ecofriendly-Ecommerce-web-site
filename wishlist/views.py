from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from store.models import Product  # Replace with your product model import
from django.contrib import messages

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_url = request.POST.get('product_url')

        if not Wishlist.objects.filter(user=request.user, product_name=product_name).exists():
            Wishlist.objects.create(user=request.user, product_name=product_name, product_url=product_url)
            messages.success(request, f'"{product_name}" added to your wishlist.')
        else:
            messages.info(request, f'"{product_name}" is already in your wishlist.')
        
        return redirect('wishlist')
    return redirect('home')

@login_required
def remove_from_wishlist(request, item_id):
    Wishlist.objects.filter(id=item_id, user=request.user).delete()
    return redirect('wishlist')
