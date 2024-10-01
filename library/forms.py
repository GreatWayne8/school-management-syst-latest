from django import forms
from .models import Ebook, Category

class EbookForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Ebook
        fields = ['title', 'author', 'category', 'file']