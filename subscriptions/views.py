from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subscription
from datetime import date, timedelta

PLANS = {
    'monthly': {'price': 10, 'days': 30},
    'yearly': {'price': 100, 'days': 365},
}

@login_required
def plans_view(request):
    subscription = Subscription.objects.filter(user=request.user).first()
    return render(request, 'subscriptions/plans.html', {
        'subscription': subscription,
        'plans': PLANS
    })

@login_required
def subscribe_view(request, plan):
    if plan not in PLANS:
        return redirect('plans')
    
    renewal = date.today() + timedelta(days=PLANS[plan]['days'])
    
    sub, created = Subscription.objects.get_or_create(user=request.user)
    sub.plan = plan
    sub.status = 'active'
    sub.renewal_date = renewal
    sub.amount_paid = PLANS[plan]['price']
    sub.save()
    
    messages.success(request, f'Successfully subscribed to {plan} plan!')
    return redirect('dashboard')

@login_required
def cancel_view(request):
    sub = Subscription.objects.filter(user=request.user).first()
    if sub:
        sub.status = 'cancelled'
        sub.save()
        messages.success(request, 'Subscription cancelled.')
    return redirect('dashboard')