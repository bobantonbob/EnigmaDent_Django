from django import forms
from .models import Response


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['name', 'email', 'response', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'modern-input', 'placeholder': "Ваше ім'я"}),
            'email': forms.EmailInput(attrs={'class': 'modern-input', 'placeholder': 'Email (необов’язково)'}),
            'response': forms.Textarea(attrs={'class': 'modern-textarea', 'placeholder': 'Ваш відгук про Enigma Dent', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'modern-file', 'accept': 'image/*'}),
        }
