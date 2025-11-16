from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Author, CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'date_of_birth', 'profile_photo', 'password1', 'password2']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
