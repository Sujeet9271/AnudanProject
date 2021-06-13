from django.shortcuts import redirect, render
from .models import PalikaUser
from .forms import CustomUserCreationForm
from django.contrib import messages


# Create your views here.

def staff_registration(request):
    context = {}
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success('Staff User Created')
            return redirect('index')
        else:
            form = CustomUserCreationForm()
            context['form'] = form
    else:
        form = CustomUserCreationForm()
        context['form'] = form
    return render(request,'staff_registration.html',context)
        
