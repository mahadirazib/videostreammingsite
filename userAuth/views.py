from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . import models
from .forms import userform, userformMoreinfo


# Create your views here.


def registrationFunction(request):

    userForm = userform
    userForm2 = userformMoreinfo
    dict = {'userform': userForm, 'userform2': userForm2, 'btntext': "Register", 'register': True}


    if request.method == 'POST':

        userForm = userform(data=request.POST)
        userInfoForm = userformMoreinfo(data=request.POST)


        if userForm.is_valid() and userInfoForm.is_valid():

            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            userInfo = userInfoForm.save(commit=False)
            userInfo.user = user

            if 'proPic' in request.FILES:
                userInfo.proPic = request.FILES['proPic']

            userInfo.save()

            return HttpResponseRedirect(reverse('userAuth:loginFunction'))
    
        else:
            userForm = userform(request.POST)
            userInfoForm = userformMoreinfo(request.POST)


    
    return render(request, 'authentication/registerAndEditUser.html', context=dict)





def loginFunction(request):

    diction = {'username': '', 'password': ''}
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        diction.update({'username': username})
        diction.update({'password': password})

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('feed:feedMain'))
            else:
                diction.update({'message': "Account is not active"})

        else:
            diction.update({'message': "Password or username may be wrong"})

        
    return render(request, 'authentication/loginApp.html', context=diction)



@login_required
def editFunction(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.all()
    currentUserMoreInfo = models.userInfo.objects.get(user = currentUser)

    userForm = userform(instance=currentUser)
    userForm2 = userformMoreinfo(instance=currentUserMoreInfo)

    dict = {'userform': userForm, 'userform2': userForm2, 'btntext': "Save"}


    if request.method == 'POST':

        userForm = userform(data=request.POST, instance=currentUser)
        userInfoForm = userformMoreinfo(data=request.POST, instance=currentUserMoreInfo)


        if userForm.is_valid() and userInfoForm.is_valid():

            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            userInfo = userInfoForm.save(commit=False)
            userInfo.user = user

            if 'proPic' in request.FILES:
                userInfo.proPic = request.FILES['proPic']

            userInfo.save()

            return HttpResponseRedirect(reverse('userAuth:loginFunction'))
    
        else:
            userForm = userform(data=request.POST)
            userInfoForm = userformMoreinfo(data=request.POST)
            dict.update({'userform': userForm, 'userform2': userInfoForm})

    
    return render(request, 'authentication/registerAndEditUser.html', context=dict)




@login_required
def logoutFunction(request):
    logout(request)
    return HttpResponseRedirect(reverse('userAuth:loginFunction'))

