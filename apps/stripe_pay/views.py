from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_checkout_session(request, *args, **kwargs):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, price_1234) of the product you want to sell
                    'price': 'price_1RaNpYQRg5XXScsnuKePhsIC',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{settings.BASE_URL}{reverse("success")}?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{settings.BASE_URL}{reverse("cancel")}',
        )
        return redirect(checkout_session.url, code=303)
    
    except Exception as e:
        return HttpResponse(str(e), status=400)
    
def checkout(request):
    return render(request, 'stripe_pay/checkout.html')

def success(request):
    return render(request, 'stripe_pay/success.html')

def cancel(request):
    return render(request, 'stripe_pay/cancel.html')
