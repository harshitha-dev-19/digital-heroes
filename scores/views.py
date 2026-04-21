from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Score
from .forms import ScoreForm

@login_required
def add_score(request):
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            # Check 5-score rolling limit
            user_scores = Score.objects.filter(user=request.user)
            if user_scores.count() >= 5:
                oldest = user_scores.last()
                oldest.delete()
            score = form.save(commit=False)
            score.user = request.user
            score.save()
            messages.success(request, 'Score added successfully!')
            return redirect('dashboard')
    else:
        form = ScoreForm()
    return render(request, 'scores/add_score.html', {'form': form})

@login_required
def edit_score(request, pk):
    score = get_object_or_404(Score, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            messages.success(request, 'Score updated!')
            return redirect('dashboard')
    else:
        form = ScoreForm(instance=score)
    return render(request, 'scores/add_score.html', {'form': form})

@login_required
def delete_score(request, pk):
    score = get_object_or_404(Score, pk=pk, user=request.user)
    score.delete()
    messages.success(request, 'Score deleted!')
    return redirect('dashboard')