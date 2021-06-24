from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
import random
from django.core.mail import EmailMessage
import threading
from django.utils.translation import gettext as _
class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send(email,otp):
    subject = 'Login OTP'
    otp = otp
    message = f'Here is the login otp for anudan project {otp}.'
    email = EmailMessage(subject=subject ,body=message, from_email='sujeet9271@gmail.com',to=[email])
    EmailThread(email).start()


def generate_otp(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user:
            if user.is_active:
                request.session['username'] = email
                request.session['password'] = password
                otp = random.randint(100000,999999)
                request.session['otp'] = otp
                send(email=user.email,otp=otp)                
                messages.success(request,_('An OTP is sent to the registered email.'))
                # login(request,user)
                return redirect('otp')
        else:
            messages.error(request,_('username or password not correct'))
            return redirect('admin:login')    
                
    else:
        form = AuthenticationForm()
    return render(request,'admin/login.html',{'form':form})


def otp(request):
    if request.method=='POST':
        otp = request.session['otp']
        otp_post = int(request.POST['otp'])
        if otp==otp_post:
            email = request.session['username']
            password = request.session['password']
            user = authenticate(email=email,password=password)
            login(request,user)
            request.session.delete('otp')
            return redirect('admin:index')
        else:
            email = request.session['username']
            password = request.session['password']
            user = authenticate(email=email,password=password)
            otp = random.randint(100000,999999)
            request.session['otp'] = otp
            send(email=user.email,otp=otp)
            messages.error(request,_('Invalid OTP, Check your email for new otp'))
    return render(request,'admin/otp.html')
            
