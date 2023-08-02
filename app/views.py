from django.shortcuts import render

# Create your views here.
from app.models import *
from app.forms import *
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def Registration(request):
    d={'USFO':UserForm(),'PFO':ProfileForm()}
    if request.method=='POST' and request.FILES:
        USFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if USFD.is_valid() and PFD.is_valid():
            NSUFO=USFD.save(commit=False)
            submittedPW=USFD.cleaned_data['password']
            NSUFO.set_password(submittedPW)
            NSUFO.save()
            NSPO=PFD.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()

            send_mail('Registration',
                      'You Are Registration is Successfull',
                      'vijaymuneppa2062001@gmail.com',
                      [NSUFO.email],
                      fail_silently=True)
            return HttpResponse('Done')
        
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_details(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_details.html',d)

@login_required
def change_password(request):
    if request.method=="POST":
        pw=request.POST.get('pw')
        us=request.session.get('username')
        UO=User.objects.get(username=us)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Change Password Done')
    return render(request,'change_pw.html')



def Reset_password(request):
    if request.method=='POST':
        UN=request.POST.get('na')
        PW=request.POST.get('pw')
        RPW=request.POST.get('rpw')
        LUO=User.objects.filter(username=UN)
        if LUO:
            if PW==RPW:
                UO=LUO[0]
                UO.set_password(PW)
                UO.save()
                return HttpResponse('Password Reset Done')
            else:
                return HttpResponse('Password Mis-match')
        else:
            return HttpResponse('Invalid Password')
    return render(request,'reset_pw.html')