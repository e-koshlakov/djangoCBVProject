from django import forms
from reviews.models import Review
from dogs.forms import StyleFormMixin

class ReviewForm(StyleFormMixin, forms.ModelForm):
    title = forms.CharField(label='Заголовок', max_length=150)
    content = forms.TextInput()
    slug = forms.SlugField(label='URL', max_length=20, initial='temp_slug', widget=forms.HiddenInput)
    class Meta:
        model = Review
        fields = ('dog', 'title', 'content', 'slug',)