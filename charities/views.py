from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Charity
from accounts.models import Profile

def charity_list(request):
    query = request.GET.get('q', '')
    charities = Charity.objects.filter(name__icontains=query) if query else Charity.objects.all()
    return render(request, 'charities/list.html', {
        'charities': charities,
        'query': query
    })

@login_required
def select_charity(request, pk):
    charity = get_object_or_404(Charity, pk=pk)
    profile = Profile.objects.get_or_create(user=request.user)[0]
    profile.selected_charity = charity
    profile.save()
    messages.success(request, f'{charity.name} selected as your charity!')
    return redirect('dashboard')