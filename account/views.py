from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from account.forms import CommonUserProfileForm, UserProfileSocialLinksFormSet, ProfileCompleteForm, LoginForm, \
    UserRegistrationForm
from account.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username").lower()
            password = form.cleaned_data.get("password").lower()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'nom d\'utilisateur ou mot de passe incorrect'
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Erreur de validation du formulaire'
            )
    return render(request, "account/login.html", {"form": form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password1'])
            new_user.save()
            auth_user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1']
            )
            if auth_user is not None:
                login(request, auth_user)
            if auth_user.is_staff:
                return redirect('account:dashboard')#
            else:
                return redirect('account:profile_complete')
        else:
            return render(request, 'account/signup.html', {'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/signup.html', {'user_form': user_form})


def profile_complete(request):
    ctx = {}
    user = User.objects.get(pk=request.user.pk)

    try:
        profile_edit_form = CommonUserProfileForm(
            instance=user.profile
        )
        social_links_form = UserProfileSocialLinksFormSet(
            instance=user.profile
        )
        ctx.update({
            'profile_edit_form': profile_edit_form,
            'social_links_form': social_links_form
        })
    except:
        messages.add_message(
            request,
            messages.INFO,
            "Maybe your account is not verified yet, please check your badge."
        )

    verification_form = ProfileCompleteForm(instance=user)
    if request.method == 'POST':
        verification_form = ProfileCompleteForm(
            request.POST,
            instance=user
        )
        if 'user-profile-update-form' in request.POST:
            profile_edit_form = CommonUserProfileForm(
                request.POST,
                request.FILES,
                instance=user.profile
            )
            social_links_form = UserProfileSocialLinksFormSet(
                request.POST,
                instance=user.profile
            )
            if profile_edit_form.is_valid():
                profile_edit_form.save()

            if social_links_form.is_valid():
                social_links_form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                'Your profile has been saved.'
            )
            return redirect('account:profile_complete')
        else:
            if verification_form.is_valid():
                verification_form.instance.approval_status = 'p'
                # approval status get's pending
                verification_form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Your request has been sent, please be patient.'
                )
                return redirect('account:profile_complete')
    user_permissions = user.user_permissions.all()
    ctx.update({
        'verification_form': verification_form,
        'user_perms': user_permissions if user_permissions else None,
    })
    return render(request, 'account/profile_complete.html', ctx)
