from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render,redirect
from .forms import SignupForm,AddMemberForm
from django.contrib.auth import login,authenticate
from .models import Profile,Group,Task,ChatQuestion,Message
from .forms import ProfileForm,LoginForm,GroupForm,TaskAssignForm,TaskUpdateForm,TaskStatusForm
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
    tasks=Task.objects.filter(assigned_to=request.user).select_related('group')
    question=ChatQuestion.objects.all()

    group_id=request.GET.get('group')
    is_completed=request.GET.get('completed')
    due=request.GET.get('due')
    search=request.GET.get('search')

    if group_id:
        tasks=tasks.filter(group_id=group_id)


    if is_completed=='yes':
        tasks=tasks.filter(is_completed=True)
    elif is_completed=='no':
        tasks=tasks.filter(is_completed=False)

    if due=='today':
        today=timezone.now().date()
        tasks=tasks.filter(deadline=today)
    elif due=='this_week':
        today=timezone.now().date()
        week_end=today+timedelta(days=7)
        tasks=tasks.filter(deadline__range=[today,week_end])



    groups=Group.objects.filter(members=request.user)


    return render(request,'dashboard.html',{ 'profile_detail':profile,'tasks':tasks,'groups':groups,'questions':question,'filter_values':{
        'group':group_id,
        'completed':is_completed,
         'due':due,
            'search':search   }})




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

def add_member_view(request,group_id):
    group=get_object_or_404(Group,id=group_id)
    message=''

    if request.method=='POST':
        form=AddMemberForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            try:
                user=User.objects.get(email=email)
                if user in group.members.all():
                    message='User is already a member of the group '
                else:
                    group.members.add(user)
                    message=f"{user.username} added to group"
            except User.DoesNotExist:
                message='No user found with that email.'
    else:
        form=AddMemberForm()
    return render(request,'add_group_member.html',{
        'form':form,
        'group':group,
        'message':message
    })
    
def admin_task_status(request,task_id):
    task=get_object_or_404(Task,id=task_id)

    if request.method=='POST':
        form=TaskStatusForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('group_detail',group_id=task.group.id)
    else:
        form=TaskStatusForm(instance=task)
    return render(request,'task_status.html',{'form':form,
                                      'task':task}) 



def chat_view(request):
    user_groups=Group.objects.filter(members=request.user)
    group_members=User.objects.filter(user_groups__in=user_groups).exclude(id=request.user.id).distinct()
    selected_user_id=request.GET.get("user")
    selected_user=None
    messages=[]

    if selected_user_id:
        selected_user=get_object_or_404(User,id=selected_user_id)
        messages=Message.objects.filter(sender__in=[request.user,selected_user],
                                        receiver__in=[request.user,selected_user]).order_by("timestamp")
        
    return render(request,"chat.html",{"group_members":group_members,'messages':messages,'selected_user':selected_user})


@csrf_exempt
def send_messages(request):
    if request.method=='POST':
        receiver_id=request.POST.get("receiver_id")
        content=request.POST.get("content")
        receiver=get_object_or_404(User,id=receiver_id)
        msg=Message.objects.create(sender=request.user,receiver=receiver, content=content)
        return JsonResponse({"status": "sent", "message": msg.content, "timestamp": msg.timestamp.strftime('%H:%M')})
