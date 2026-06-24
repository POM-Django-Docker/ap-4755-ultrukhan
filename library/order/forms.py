from django import forms
from book.models import Book


class OrderForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(count__gt=0),
        label='Select Book',
        empty_label='-- Select a book --'
    )