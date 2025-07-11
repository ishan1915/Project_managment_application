from django.shortcuts import render,redirect
from .forms import SignupForm
from django.contrib.auth import login,authenticate
from .models import Profile
from .forms import ProfileForm,LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth import logout
from django.contrib import messages


 # Create your views here.
def signup_view(request):
    if request.method =='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('login')
    else:
        form=SignupForm()
    return render(request,'signup.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin-dashboard')   
                else:
                    return redirect('dashboard')
            else:
                form.add_error(None, "Invalid login credentials.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('user_login')


def dashboard_view(request):
     
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request,'dashboard.html',{ 'profile_detail':profile})




def profile_edit(request):
    try:
        profile=request.user.profile
    except Profile.DoesNotExist:
        profile=Profile(user=request.user)

    if request.method=='POST':
        profile_form=ProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,"Sucessfully Edited")
            return redirect('dashboard')
            
    else:
        profile_form=ProfileForm(instance=profile)
    
    return render(request,'edit_profile.html',{'profile_form':profile_form})


 
        

         

def admin_dashboard(request):
     
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request,'admin_dashboard.html',{ 'profile_detail':profile})



def admin_edit(request):
    try:
        profile=request.user.profile
    except Profile.DoesNotExist:
        profile=Profile(user=request.user)

    if request.method=='POST':
        profile_form=ProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,"Sucessfully Edited")
            return redirect('admin-dashboard')
    else:
        profile_form=ProfileForm(instance=profile)
    
    return render(request,'admin_edit.html',{'profile_form':profile_form})