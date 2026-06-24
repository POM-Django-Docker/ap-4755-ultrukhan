from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].label_from_instance = lambda obj: f"{obj.name} {obj.surname} {obj.patronymic}"