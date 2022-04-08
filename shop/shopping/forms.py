from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import GoodsDB, ReviewsDB


# class AddReviewForm(forms.Form):
#
#     def add_name_user(self, request):
#         ...
#
#     def add_good(self, request):
#         ...
#
#     review_title = forms.CharField(
#         max_length=150,
#         label='Заголовок отзыва',
#         widget=forms.TextInput(attrs={'class': 'form-group'})
#     )
#     rating = forms.CharField(
#         label='Рейтинг',
#         widget=forms.Select(attrs={'class': 'rating-form'})
#     )
#     text = forms.CharField(
#         label='Текст отзыва',
#         required=False,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
#     )


class AddReviewForm(forms.ModelForm):

    def add_name_user(self, request):
        user_name = self.cleaned_data['user_name']
        return user_name(request)
        ...

    def add_good(self, request):
        ...

    def add_slug(self, request):
        ...

    class Meta:
        model = ReviewsDB

        fields = ('review_title', 'rating', 'text',)
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'form-group'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'rating': forms.Select(attrs={'class': 'rating-form'}),
            'good': forms.HiddenInput(),
        }
#
#     @login_required
#     def in_form(self, request):
#         user_name = self.cleaned_data['user_name']
#         if request.user.is_authenticated():
#             user_name = User.objects.get(user=request.user)
#             print(1234567)
#             print(request)
#             return user_name
#         else:
#             print(7654321)



    # @login_required
    # def show_form(self, request):
    #     if request.method == 'GET':
    #         form = AddReviewForm()
    #         # return render(request, 'shopping/show_good.html', {'form': form})
    #
    #     elif request.method == 'POST':
    #         form = AddReviewForm(request.POST)
    #         if form.is_valid():
    #             post = form.save(commit=False)
    #             post.current_user = User.objects.get(user=request.user)
    #             post.save()
    #             return redirect('index')

