from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm #using the django in-built form which we get during the admin.
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        #In the meta class, we define the model, and the fields from it we want to add.
        model = Tweet
        fields = ['text', 'photo']
        
class UserRegistrationForm(UserCreationForm):
    #specifying the fields which we want to add additionally in the in-built form.
    email = forms.EmailField()#additional  field
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    
    