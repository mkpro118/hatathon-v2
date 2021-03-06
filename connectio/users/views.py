from django.shortcuts import (render,
                              # HttpResponse,
                              redirect,)
from django.http import JsonResponse
from .models import NewUser, Profile as UserProfiles
from interface.models import Events
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate, logout


# Create your views here.


def Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        context = {
            'site_title': 'Register - Connectio',
        }
        return render(request, 'users/register.html', context)


def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        context = {
            'site_title': 'Login - Connectio',
        }
        return render(request, 'users/login.html', context)


@login_required(login_url='login')
def Logout(request):
    logout(request)
    context = {
        'site_title': 'Logout - Connectio',
    }
    return render(request, 'users/logout.html', context)


@login_required(login_url='login')
def Profile(request, username):
    if request.method == 'POST':
        return redirect('profile')
    else:
        _user = NewUser.objects.get(username__exact=username)
        profile = _user.profile
        events = Events.objects.filter(host=_user).order_by('date')
        context = {
            'site_title': f"@{username}'s Profile - Connectio",
            'image': profile.image.url,
            'username': profile.username,
            'name': profile.name,
            'bio': profile.bio,
            'owner': request.user.username == username,
            'events': events,
        }
        return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def DefaultProfile(request):
    return redirect(f'profile/{request.user.username}')


@login_required(login_url='login')
def Edit(request, name, email, bio, location):
    acc = NewUser.objects.get(username=request.user.username)
    acc.profile.name = name
    acc.profile.bio = bio
    acc.profile.location = location
    acc.save()
    return JsonResponse({})


def check_username_availability(request, username):
    username_to_check = username
    taken = NewUser.is_username_taken(username_to_check)
    return JsonResponse({'taken': taken})


def check_email_availability(request, email):
    email_to_check = email
    taken = NewUser.is_email_taken(email_to_check)
    return JsonResponse({'taken': taken})


def register_user(request, username, email, password, location, bio, *args, **kwargs):
    username = username.lower()
    email = email.lower()
    new_user = NewUser.objects.create_user(username, email, password)
    new_user.save()
    new_user.profile.location = location
    new_user.profile.bio = bio
    new_user.profile.save()
    account = authenticate(username=username, password=password)
    login(request, account)
    destination = kwargs.get('next')
    if destination:
        return JsonResponse({'next': destination})
    else:
        return JsonResponse({'next': ''})


def login_user(request, username, password, *args, **kwargs):
    account = authenticate(username=username, password=password)
    if account is not None:
        login(request, account)
        nxt = kwargs.get('next')
        if nxt:
            return JsonResponse({'successful': True, 'next': nxt})
        else:
            return JsonResponse({'successful': True, 'next': ''})
    else:
        taken = NewUser.is_username_taken(username)
        if taken:
            return JsonResponse({'successful': False, 'username_valid': taken, 'password_valid': False})
        else:
            return JsonResponse({'successful': False, 'username_valid': taken, 'password_valid': True})
