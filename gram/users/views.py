from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from pkg_resources import _
from .forms import SignupForm, UserForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Post, Image
from .services import is_current_user, send_email, is_valid_token


def registration(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email(request, user, form)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
        return render(request, 'registration/registration.html', {'form': form})


def activate(request, uidb64, token):
    user = is_valid_token(uidb64, token)
    if user:
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('edit_profile', user.pk)
    else:
        return HttpResponse('Activation link is invalid!')


def profile_page(request, pk):
    user_page = User.objects.get(id=pk)
    posts = Post.objects.filter(author=user_page).all().order_by('-pk')
    images = Image.objects.all()
    context = {
        'posts': posts,
        'images': images,
        'user_page': user_page,
        'can_edit': is_current_user(request.user, user_page),
    }
    return render(request, "registration/profile.html", context)


def edit_profile(request, pk):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_page', pk=pk)
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
