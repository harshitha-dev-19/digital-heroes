from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Draw, Winner
from subscriptions.models import Subscription
from scores.models import Score
from datetime import date
import random

def get_prize_pool(draw):
    active_subs = Subscription.objects.filter(status='active').count()
    total_pool = active_subs * 10  # £10 per subscriber
    return {
        'total': total_pool,
        'five_match': total_pool * 0.40,
        'four_match': total_pool * 0.35,
        'three_match': total_pool * 0.25,
    }

def run_draw_logic(draw):
    # Get all active subscribers with scores
    active_users = Subscription.objects.filter(status='active').values_list('user', flat=True)
    
    # Generate 5 random winning numbers (1-45)
    winning_numbers = random.sample(range(1, 46), 5)
    draw.winning_numbers = winning_numbers
    draw.save()

    pool = get_prize_pool(draw)
    five_winners, four_winners, three_winners = [], [], []

    for user_id in active_users:
        user_scores = list(
            Score.objects.filter(user_id=user_id)
            .values_list('score', flat=True)
        )
        if not user_scores:
            continue
        matches = len(set(user_scores) & set(winning_numbers))
        if matches >= 5:
            five_winners.append(user_id)
        elif matches == 4:
            four_winners.append(user_id)
        elif matches == 3:
            three_winners.append(user_id)

    # Create winner records
    def create_winners(user_ids, match_type, pool_amount):
        if not user_ids:
            return
        prize = pool_amount / len(user_ids)
        for uid in user_ids:
            Winner.objects.get_or_create(
                draw=draw, user_id=uid, match_type=match_type,
                defaults={'prize_amount': prize}
            )

    create_winners(five_winners, '5', pool['five_match'])
    create_winners(four_winners, '4', pool['four_match'])
    create_winners(three_winners, '3', pool['three_match'])

    return winning_numbers

@login_required
def draw_list(request):
    draws = Draw.objects.filter(status='published').order_by('-month')
    return render(request, 'draws/list.html', {'draws': draws})

@login_required
def draw_detail(request, pk):
    draw = get_object_or_404(Draw, pk=pk)
    winners = Winner.objects.filter(draw=draw)
    pool = get_prize_pool(draw)
    user_winner = winners.filter(user=request.user).first()
    return render(request, 'draws/detail.html', {
        'draw': draw,
        'winners': winners,
        'pool': pool,
        'user_winner': user_winner,
    })

@staff_member_required
def admin_draws(request):
    draws = Draw.objects.all().order_by('-month')
    return render(request, 'draws/admin_draws.html', {'draws': draws})

@staff_member_required
def create_draw(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        draw = Draw.objects.create(month=month)
        messages.success(request, 'Draw created!')
        return redirect('admin_draws')
    return render(request, 'draws/create_draw.html')

@staff_member_required
def simulate_draw(request, pk):
    draw = get_object_or_404(Draw, pk=pk)
    winning_numbers = run_draw_logic(draw)
    draw.status = 'simulated'
    draw.save()
    messages.success(request, f'Simulation done! Winning numbers: {winning_numbers}')
    return redirect('admin_draws')

@staff_member_required
def publish_draw(request, pk):
    draw = get_object_or_404(Draw, pk=pk)
    draw.status = 'published'
    draw.save()
    messages.success(request, 'Draw published!')
    return redirect('admin_draws')

@login_required
def upload_proof(request, winner_id):
    winner = get_object_or_404(Winner, pk=winner_id, user=request.user)
    if request.method == 'POST':
        if 'proof_image' in request.FILES:
            winner.proof_image = request.FILES['proof_image']
            winner.status = 'pending'
            winner.save()
            messages.success(request, 'Proof uploaded! Awaiting admin review.')
            return redirect('dashboard')
    return render(request, 'draws/upload_proof.html', {'winner': winner})

@staff_member_required
def verify_winners(request):
    winners = Winner.objects.filter(status='pending')
    return render(request, 'draws/verify_winners.html', {'winners': winners})

@staff_member_required
def approve_winner(request, winner_id):
    winner = get_object_or_404(Winner, pk=winner_id)
    winner.status = 'verified'
    winner.save()
    messages.success(request, f'{winner.user.username} approved!')
    return redirect('verify_winners')

@staff_member_required
def reject_winner(request, winner_id):
    winner = get_object_or_404(Winner, pk=winner_id)
    winner.status = 'rejected'
    winner.save()
    messages.success(request, f'{winner.user.username} rejected.')
    return redirect('verify_winners')

@staff_member_required
def mark_paid(request, winner_id):
    winner = get_object_or_404(Winner, pk=winner_id)
    winner.status = 'paid'
    winner.save()
    messages.success(request, f'{winner.user.username} marked as paid!')
    return redirect('verify_winners')