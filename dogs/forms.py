from django import forms
from dogs.models import Dog

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
