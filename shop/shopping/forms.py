from django import forms

from .models import ReviewsDB


class AddReviewForm(forms.ModelForm):

    class Meta:
        model = ReviewsDB
        fields = ('review_title', 'review_rating', 'review_text',)
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'form-group'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'cols': 5, 'rows': 6}),
            'review_rating': forms.Select(attrs={'class': 'rating-form'}),
        }
