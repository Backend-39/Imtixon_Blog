from django.contrib.auth.models import User
from .models import Tag
from django import forms
import re




class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Parolni tasdiqlang')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            'email',
            'username',
            'password'
        ]
        help_texts = {
            'username': "Harflar, raqamlar va @/./+/-/_ belgilar. Ko'pi bilan 150ta belgi."
        }
        labels = {
            'username': 'Foydalanuvchi nomi:',
            'first_name': 'Ism:',
            'last_name': 'Familiya:',
            'password': 'Parol'
        }
        error_messages = {
            'username': {
                'required': "Foydalanuvchi nomi kiritilishi shart!",
                'max_length': "Foydalanuvchi nomi maksimal 150 ta belgidan oshmasligi kerak!",
                'unique': "Bunday foydalanuvchi tizimda mavjud!",
            },
            'password': {
                'required': "Parol kiritilishi shart!",
            },
            'email': {
                'required': "Email kiritilishi shart!",
                'invalid': "To‘g‘ri email manzil kiriting!",
            },
            'first_name': {
                'required': "Ism kiritilishi shart!",
                'max_length': "Ism maksimal 150 ta belgidan oshmasligi kerak!",
            },
            'last_name': {
                'required': "Familiya kiritilishi shart!",
                'max_length': "Familiya maksimal 150 ta belgidan oshmasligi kerak!",
            },
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        username = cleaned_data.get('username')
        if not password_confirm == password:
            raise forms.ValidationError("Parol va Tasdiqlovchi parol mos emas!")
        
        return cleaned_data

    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
    


class ArticleTagForm(forms.Form):
    title = forms.CharField(max_length=50)
    context = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 5
            }
        )
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    article_type = forms.ChoiceField(
        choices=[
            ('shaxsiy', 'Shaxsiy'),
            ('ommaviy', 'Ommaviy')
        ]
    )



def validate_username(value):
    pattern = r'^[\w.@+-]+$' 
    if re.match(pattern, value):
        return True
    return False


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Foydalanuvchi nomi',
        widget=forms.TextInput(
            attrs={
                'required': True,
                'placeholder': 'user12'
            }
        ),
        error_messages={
            'required': "Foydalanuvchi nomi kiritilishi shart!"
        }
    )
    password = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(
            attrs={
                'required': True
            }
        ),
        error_messages={
            'required': "Foydalanuvchi nomi kiritilishi shart!"
        }
    )

    def clean(self):
        data = super().clean()
        username = data.get('username')

        if not validate_username(username):
            raise forms.ValidationError("Foydalanuvchi nomi noto'g'ri formatda kiritildi!")
            
        return data