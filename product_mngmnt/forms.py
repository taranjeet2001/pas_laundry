from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields=['username']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
