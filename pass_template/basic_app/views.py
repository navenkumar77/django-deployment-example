from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login,logout,authenticate

def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    registered = False

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        profile_pic = UserProfileInfoForm(data=request.POST)

        if userform.is_valid() and profile_pic.is_valid():
            # Save the user form
            user = userform.save()
            user.set_password(user.password)  # Hash the password
            user.save()

            # Save the profile picture form
            profile = profile_pic.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            # Registration was successful
            registered = True

        else:
            # If forms are not valid, print errors to console and return the form with errors
            print(userform.errors, profile_pic.errors)

        # Whether the form is valid or not, return the form back to the user
        return render(request, 'basic_app/registration.html', {
            'userform': userform,
            'profile_pic': profile_pic,
            'registered': registered
        })

    else:
        # For GET request, provide empty forms
        userform = UserForm()
        profile_pic = UserProfileInfoForm()

    # Render the registration page with the forms
    return render(request, 'basic_app/registration.html', {
        'userform': userform,
        'profile_pic': profile_pic,
        'registered': registered
    })

@login_required
def special(request):
    return HttpResponse("YOU ARE LOGGED IN NICE!!!")
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("SOMEONE TRIED TO LOGIN AND FAILED")
            print("USername is {} and password is {}".format(username,password))
            return HttpResponse("INVALID LOGIN DETAILS SUPPLIED")
    else:
        return render(request,'basic_app/login.html',{})
            

