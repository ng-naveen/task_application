from django.shortcuts import render, redirect
from django.views.generic import View
from task_web_application.forms import SignUpForm, SignInForm, TaskForm, TaskEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from api.models import TaskModel
from django.utils.decorators import method_decorator
from django.contrib import messages


def signin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        return func(request, *args, **kwargs)
    return wrapper


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        return render(request, 'signup.html', {'signup_form':signup_form})
    
    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            User.objects.create_user(**signup_form.cleaned_data)
            messages.success(request, 'Account created successfully!')
            return redirect('signin')
        messages.error(request, 'We couldn’t create your account. Check your details and try again.')
        return render(request, 'signup.html', {'signup_form':signup_form})


class SignInView(View):
    def get(self, request, *args, **kwargs):
        signin_form = SignInForm()
        return render(request, 'signin.html', {'signin_form':signin_form})
    
    def post(self, request, *args, **kwargs):
        signin_form = SignInForm(request.POST)
        if signin_form.is_valid():
            print('inside')
            username = signin_form.cleaned_data.get('username')
            password = signin_form.cleaned_data.get('password')
            user_obj = authenticate(request, username=username, password=password)
            if user_obj:
                print('inside')
                login(request, user_obj)
                messages.success(request, 'You’re logged in!')
                return redirect('home')
        messages.error(request, 'Login failed. Please check your username and password.')
        return render(request, 'signin.html', {'signin_form':signin_form})
    
@method_decorator(signin_required, name='dispatch')
class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You’re logged out')
        return redirect('signin')

@method_decorator(signin_required, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')
    
@method_decorator(signin_required, name='dispatch')
class CreateTaskView(View):
    def get(self, request, *args, **kwargs):
        task_form = TaskForm()
        return render(request, 'task-add.html', {'task_form':task_form})
    
    def post(self, request, *args, **kwargs):
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.instance.user = request.user
            task_form.save()
            messages.success(request, 'New task created!')
            return redirect('task-list')
        messages.error(request, 'Error: Unable to create task. Check your input and try again.')
        return render(request, 'task-add.html', {'task_form':task_form})

@method_decorator(signin_required, name='dispatch')
class ListTaskView(View):
    def get(self, request, *args, **kwargs):
        task_objs = TaskModel.objects.filter(user=request.user).order_by('-created_date')
        return render(request, 'task-list.html', {'task_objs':task_objs})
    
@method_decorator(signin_required, name='dispatch')
class DetailTaskView(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task_obj = TaskModel.objects.get(id=task_id)
        return render(request, 'task-details.html', {'task_obj':task_obj})

@method_decorator(signin_required, name='dispatch')
class UpdateView(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task_obj = TaskModel.objects.get(id=task_id)
        task_form = TaskEditForm(instance=task_obj)
        return render(request, 'task-update.html', {'task_form':task_form})
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task_obj = TaskModel.objects.get(id=task_id)
        task_form = TaskEditForm(request.POST, instance=task_obj)
        if task_form.is_valid():
            task_form.save()
            messages.success(request, 'Task updated!')
            return redirect('task-list')
        messages.error(request, 'Task update failed. Please try again.')
        return render(request, 'task-update.html', {'task_form':task_form})

@method_decorator(signin_required, name='dispatch')
class DeleteTaskView(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        TaskModel.objects.get(id=task_id).delete()
        messages.success(request, 'Task deleted!')
        return redirect('task-list')
    