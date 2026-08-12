from django import forms
from .models import Articles, ResponseSite


class ArticlesForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label='Я погоджуюсь на обробку персональних даних для зв’язку та запису на прийом.',
        widget=forms.CheckboxInput(attrs={'class': 'modern-checkbox'})
    )

    class Meta:
        model = Articles
        fields = ['title', 'phone', 'email', 'about', 'preferred_time', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'modern-input', 'placeholder': "Ваше ім’я та прізвище"}),
            'phone': forms.TextInput(attrs={'class': 'modern-input', 'placeholder': '+38 (___) ___-__-__', 'inputmode': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'modern-input', 'placeholder': 'Email (необов’язково)'}),
            'about': forms.TextInput(attrs={'class': 'modern-input', 'placeholder': 'Наприклад: лікування карієсу, консультація, протезування'}),
            'preferred_time': forms.TextInput(attrs={'class': 'modern-input', 'placeholder': 'Наприклад: завтра після 16:00'}),
            'message': forms.Textarea(attrs={'class': 'modern-textarea', 'rows': 5, 'placeholder': 'Коротко опишіть питання або побажання'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Вкажіть коректний номер телефону.')
        return phone


class ResponseSiteForm(forms.ModelForm):
    class Meta:
        model = ResponseSite
        fields = ['title', 'about', 'message']
