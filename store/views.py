from django.shortcuts import render, get_object_or_404,redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

def product_list(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request
    if query:
        # Filter products based on search query
        products = Product.objects.filter(name__icontains=query)  # Case-insensitive search
    else:
        # Show all products if no query is provided 
        products = Product.objects.all()

    return render(request, 'store/product_list.html', {'products': products, 'query': query})

def category_products(request, category_code):
    products = Product.objects.filter(category=category_code)
    category_name = dict(Product._meta.get_field('category').choices).get(category_code, 'Unknown Category')
    context = {
        'products': products,
        'category_name': category_name,
    }
    return render(request, 'store/category_products.html', context)


# @login_required
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_details.html', {'product': product})

def about_view(request):
    return render(request, 'about.html')

from django.http import HttpResponse

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Optional: Process form data (e.g., save to database)
        full_message = f"Message from {name} ({email}):\n\n{message}"

        try:
            # Example: Send an email (configure email settings in settings.py)
            send_mail(
                subject=subject,
                message=full_message,
                from_email=email,  # Use the user's email
                recipient_list=['your-email@example.com'],  # Replace with your email
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        # Redirect to contact page after submission
        return redirect('contact')
    
    # If GET request, just render the contact page
    return render(request, 'contact.html')

def thank_you_view(request):
    return render(request, 'thank_you.html')