from django.forms import ModelForm, Textarea,TextInput
from django import forms
from django.contrib.auth.models import Permission, Group
from administration.models import User

class UploadPortrainForm(forms.Form):
	portrain 	= forms.FileField()



class GroupForm(ModelForm): 
    class Meta:
        model = Group
        fields = ['name', 'permissions']

 
class UserForm(ModelForm): 
    class Meta:
        model = User
        #fields = ['email', 'date', 'is_active', 'is_admin', 'name',
        #          'is_head_portrait', 'group']
        exclude = ['password', 'head_portrait','fake_head_portrait', 'date',
                   'last_login']
