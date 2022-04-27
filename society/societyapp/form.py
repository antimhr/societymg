from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content')
        widgets = {
            'title':
                forms.TextInput(attrs={'class': 'title-control', 'placeholder': 'Title of the News...'}),
            'content':
                forms.Textarea(attrs={'class': 'content-control', 'placeholder': 'Content of the New...'}),
        }
