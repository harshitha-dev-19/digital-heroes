from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from charities.models import Charity
from scores.models import Score
from subscriptions.models import Subscription
from draws.models import Draw, Winner
from accounts.models import Profile

def home_view(request):
    featured_charities = Charity.objects.filter(is_featured=True)[:3]
    return render(request, 'home/home.html', {
        'featured_charities': featured_charities
    })

@login_required
def dashboard_view(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    scores = Score.objects.filter(user=request.user)[:5]
    subscription = Subscription.objects.filter(user=request.user).first()
    winners = Winner.objects.filter(user=request.user)
    return render(request, 'home/dashboard.html', {
        'profile': profile,
        'scores': scores,
        'subscription': subscription,
        'winners': winners,
    })

@staff_member_required
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'active_subs': Subscription.objects.filter(status='active').count(),
        'total_subs': Subscription.objects.count(),
        'total_charities': Charity.objects.count(),
        'pending_winners': Winner.objects.filter(status='pending').count(),
        'total_draws': Draw.objects.count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_subs': Subscription.objects.order_by('-start_date')[:5],
        'prize_pool': Subscription.objects.filter(status='active').count() * 10,
    }
    return render(request, 'home/admin_dashboard.html', context)