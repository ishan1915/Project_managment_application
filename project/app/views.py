from django.shortcuts import render,redirect
from .forms import SignupForm
from django.contrib.auth import login
from .models import Profile
from .forms import ProfileForm
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





def dashboard_view(request):
     
    profile_detail=Profile.objects.get(user=request.user)
    return render(request,'dashboard.html',{ 'profile_detail':profile_detail})




def profile_edit(request):
    try:
        profile=request.user.profile
    except Profile.DoesNotExist:
        profile=Profile(user=request.user)

    if request.method=='POST':
        profile_form=ProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('dashboard')
    else:
        profile_form=ProfileForm(instance=profile)
    
    return render(request,'edit_profile.html',{'profile_form':profile_form})

            
            
        

         

