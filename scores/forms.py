from django import forms
from .models import Score

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score < 1 or score > 45:
            raise forms.ValidationError('Score must be between 1 and 45.')
        return score