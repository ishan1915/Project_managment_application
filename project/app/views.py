from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect

from .forms import SignupForm
from django.contrib.auth import login,authenticate
from .models import Profile,Group,Task
from .forms import ProfileForm,LoginForm,GroupForm,TaskAssignForm,TaskUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User

 # Create your views here.
def signup_view(request):
    if request.method =='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('user_login')
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
    tasks=Task.objects.filter(assigned_to=request.user)
    return render(request,'dashboard.html',{ 'profile_detail':profile,'tasks':tasks})




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
    groups=Group.objects.filter(members=request.user)
    tasks=Task.objects.filter(group__in=groups)
    return render(request,'admin_dashboard.html',{ 'profile_detail':profile,'groups':groups,'tasks':tasks})



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



def create_group_view(request):
    if request.method=='POST':
        form=GroupForm(request.POST)
        member_emails=request.POST.getlist('member_email')
        if form.is_valid():
            group=form.save()
            for email in member_emails:
                try:
                    user=User.objects.get(email=email.strip())
                    group.members.add(user)
                except User.DoesNotExist:
                    continue
            group.save()
            return redirect('admin-dashboard')
    else:
        form=GroupForm()
    return render(request,'create_group.html',{'form':form})


def get_group_members(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        members = group.members.all()
        data = {
            "members": [{"id": user.id, "username": user.username} for user in members]
        }
        return JsonResponse(data)
    except Group.DoesNotExist:
        return JsonResponse({"members": []})


def assign_task_view(request):
    if request.method == 'POST':
        form = TaskAssignForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if task.assigned_to in task.group.members.all():
                task.save()
                return redirect('admin_dashboard')
            else:
                form.add_error('assigned_to', 'User is not a member of the selected group.')
    else:
        form = TaskAssignForm()
        form.fields['assigned_to'].queryset = User.objects.none()
    return render(request, 'assign_task.html', {'form': form})


@login_required
def update_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            #task.is_completed = True
            task.save()
            return redirect('dashboard')
    else:
        form = TaskUpdateForm(instance=task)
    return render(request, 'update_task.html', {'form': form})




def group_detail_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    tasks = Task.objects.filter(group=group).select_related('assigned_to')
    return render(request, 'group_detail.html', {
        'group': group,
        'tasks': tasks
    })