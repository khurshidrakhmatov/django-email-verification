from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.contrib.auth import authenticate, login 
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from questions.models import  Question
from answers.models import Answer, Reply
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



#-----------------------------------------------------------------------------

class ProfileEditView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = "edit-profile.html"
    def get_object(self):

        object = get_object_or_404(User, username=self.kwargs.get("username"))

        # only owner can view his page
        if self.request.user.username == object.username:
            return object
        else:
            # redirect to 404 page
            print("you are not the owner!!")

#-----------------------------------------------------------------------------
      
def profile(request, username):
    user = get_object_or_404(User, username=username)    
    questions = Question.objects.filter(author = user).order_by("-date")
    answers  = Answer.objects.filter(author=user).order_by("-date_answered")
    
    q = questions.count()
    a = answers.count()
      
    context = {'user': user,  "a":a, "q":q, 'answers':answers, 'questions':questions} 

    return render(request, 'profile.html', context)

#-----------------------------------------------------------------------------

def get_user(request):
    user = request.user

    return {'user':user}

#-----------------------------------------------------------------------------

def my_functional_view(request):
    massage = ''
    if request.method == "POST":
     
      username = request.POST['username']
      name = request.POST['name']
      email = request.POST['email']
      password1 = request.POST['password1']
      password2 = request.POST['password2']
      if len(username) < 6:
            massage = "Your username is too short"
      elif User.objects.filter(username=username):
            massage ='This username is already taken'      
      elif len(email)< 6:
            massage = "Please enter true email address"  
      elif User.objects.filter(email=email):
            massage = "You have already an account according to your email address"      
      elif len(password1)<6:
            massage = "The password must contain 6 symbols"
      elif password1 != password2:
            massage = "The passwords don't match"    
      else:                 
            user = get_user_model().objects.create(first_name = name, username=username, password=make_password(password1), email=email)
            user.is_active = False  # Example
            user.is_staff = False
            send_email(user)
            return redirect('confirm_needed', user.id)
      
      
    return render(request, 'signup.html', {"massage":massage})

#------------------------------------------------------------------------------

def confirm_needed(request, id):
      user = User.objects.get(id=id)
      if user.is_active == True:
            return redirect('/login')
      else:
            return render(request, 'confirm_needed.html')
        
#-------------------------------------------------------------------------------     
        
def login_view(request):
    
    massage=''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user1 = User.objects.get(username=username)
        user = authenticate(request, username=username, password=password)
            
        if not user1.is_active:
            massage ='You have to confirm your account'
        elif user is not None:
            login(request, user)
            return redirect('/')
        else:
            massage = "Not found"      

    return render(request, 'login.html', {'massage':massage})          