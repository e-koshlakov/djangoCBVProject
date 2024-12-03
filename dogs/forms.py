from django import forms
from dogs.models import Dog, Parent
import datetime

from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner',)

    def clean_birth_date(self):
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']
            now_year = datetime.datetime.now().year
            if cleaned_data.year > now_year:
                raise forms.ValidationError('Дата рождения не может быть в будущем')
            if cleaned_data.year < now_year - 30:
                raise forms.ValidationError('Покойников не берем.')

            return cleaned_data
        else:
            return self.cleaned_data['birth_date']


class ParentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
