from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField()
    class Meta:
        model = CustomUser
        fields = ('email','username', 'age', 'password1', 'password2')
        
    
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.fields