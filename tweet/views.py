from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def index(request):
    return render(request,'index.html')


#(1.)functionality for listing all the tweets :->

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html', {'tweets' : tweets})

#(2.)functionality for writing tweets :->
#standard way of creating and handling forms in Django

@login_required #using decorator here.
def tweet_create(request):
    if request.method == "POST": #first-case will be resolved always, whether the form is submitted by the user or not ? 
      form = TweetForm(request.POST, request.FILES) #with POST data request , we are also excepting a file from the user.
      if form.is_valid(): #checking all the security measures for the form.
        tweet = form.save(commit=False)#COMMIT = FALSE is specifying that we are saving it but not in the database, we are saving it in some variable or somewhere else.
        tweet.user = request.user
        tweet.save()
        return redirect('tweet_list')    
    else: #second case will be resolved of sending/displaying an empty form to the user.
        form = TweetForm()
    #Third case will be resolved of rendering the form to the front-end.  
    return render(request,'tweet_form.html', {'form' : form})

#(3.)functionality of editing the existing tweet.

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id,user = request.user)#here user = request.user is specifying that the edit option is only available to the user whose tweet it is and not the tweets of the other users , we can edit.
    if request.method =="POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False) 
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')      
    else:
        form = TweetForm(instance = tweet)
    return render(request,'tweet_form.html', {'form' : form})

#(4.)Deleting the existing tweet

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
        #here no need of validating the form, because here form is not coming and we just want to delete the existing tweet.
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html',{'tweet':tweet})

 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)#we are using the built-in login form of the django
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm() 
    return render(request,'registration/register.html',{'form':form})

            
    
    
'''
In django there are some standardized methods, which tells whether the form is valid or not.
By-default django provides some built-in features like :- csrf(cross-site request forgery) security

Note :- In django, jab bhi form ek bhara jaayega uske sath automatically ek user humlog ko milta hi hai.

Note:- Yes, in Django, if you do not explicitly define an id field in your model, Django automatically adds an id field as the primary key for each object. This field is an AutoField, which generates an auto-incrementing integer value for every new object in the model.
Jinja templates are normal HTML templates in Django.As we directly embedded them in our HTML codes.

There's always a built-in model created by django itself always which is "User" model which is the path of django.contrib.auth.

Fields in the Default User Model :->

username,
first_name,
last_name,
email,
password,
is_staff, is_superuser, isactive
date_joined, last_login



django in-built user registration is very powerful in itself and using it is more beneficial.
The only drawback of it , that it takes everything based on username basis and not in email basis.But we can add that field also.

decorators in python wraps a function with a particular functionalities


What actually @login_required decorator do in django ?

--> The @login_required decorator in Django is used to restrict access to certain views to only authenticated users. It ensures that only users who have logged in can access the view it decorates.

How it works ? :->

1. Checking Authentication:

(a) When a user tries to access the view, @login_required checks if the user is authenticated.
(b) If the user is not authenticated, they are redirected to the login page.

2. Redirection to Login Page:

(a) By default, @login_required uses the LOGIN_URL setting in your Django configuration to determine where to redirect unauthenticated users.
(b) If LOGIN_URL is not set, it defaults to /accounts/login/.

3. Custom Behavior :
You can customize the @login_required decorator to specify a different redirect_field_name or login_url for specific views.

Examples :-

1) 

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def my_protected_view(request):
    return render(request, 'protected_page.html')

2) With Customizations :-

(a) Specify a Different Login URL: You can use the login_url parameter to specify a custom login page.

@login_required(login_url='/custom-login/')
def my_view(request):
    ...

(b)Redirect Field Name: Use the redirect_field_name parameter to specify the name of the query parameter that holds the URL to redirect to after login.

In Django, the cleaned_data dictionary is part of the Form class and is used to store validated and cleaned data for each field in a form. It becomes available after calling the is_valid() method on a form instance, which performs validation.

How It Works:

1.) Field Validation:

(a) When is_valid() is called, Django validates each field in the form using the field-specific validation rules (e.g., required, max_length).
(b) If all fields are valid, their cleaned values are stored in the cleaned_data dictionary.

2.) Custom Validation:

You can define custom cleaning and validation logic by overriding the clean() method or clean_<fieldname>() methods in the form

from django import forms

class MyForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    age = forms.IntegerField(required=True)

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0:
            raise forms.ValidationError("Age cannot be negative.")
        return age

# In a view:
def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():  # Triggers validation
            cleaned_data = form.cleaned_data
            name = cleaned_data.get('name')
            age = cleaned_data.get('age')
            # Process the cleaned data
        else:
            # Handle form errors
            pass

After is_valid() returns True, you can access cleaned and validated data using the cleaned_data dictionary.

Note :- Data in cleaned_data is cleaned and converted into Python data types (e.g., a date string will be converted to a datetime.date object if it's a DateField).

'''