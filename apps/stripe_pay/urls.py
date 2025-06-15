from django.urls import path
from .views import *


urlpatterns = [
    path('', checkout, name='checkout'),
    path('create-checkout-session/', create_stripe_checkout_session, name='create-checkout-session'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
]
