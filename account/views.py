from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView
from rolepermissions.roles import assign_role
from verify_email.email_handler import send_verification_email

from account.forms import CommonUserProfileForm, UserProfileSocialLinksFormSet, ProfileCompleteForm, LoginForm, \
    UserRegistrationForm, ApprovalProfileUpdateForm, UserChangeFormDashboard, UpdateUserForm
from account.models import User, CustomGroup
from permission_handlers.administrative import user_is_admin_or_su
from permission_handlers.basic import user_is_verified


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
                return redirect("home:home")
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
            first_name = user_form.cleaned_data.get("first_name")
            lastname = user_form.cleaned_data.get("last_name")
            username = user_form.cleaned_data.get("username")
            email = user_form.cleaned_data.get("email")
            address = user_form.cleaned_data.get("address")
            raw_password = user_form.cleaned_data.get("password1")

            auth_user = authenticate(
                first_name=first_name,
                lastname=lastname,
                username=username,
                password=raw_password,
                email=email,
                address=address
            )

            if auth_user is not None:
                login(request, auth_user)
            else:
                inactive_user = send_verification_email(request, user_form)

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Un email vous a été envoyer à l'adresse {email}, Veuillez confirmer votre adresse mail pour "
                    f"activer "
                    f"votre compte "
                )
                return redirect('/login')

        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Formulaire incorrect'
            )
            return render(request, 'account/signup.html', {'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/signup.html', {'user_form': user_form})


@login_required
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
            'social_links_form': social_links_form,
        })
    except:
        messages.add_message(
            request,
            messages.INFO,
            "Peut-être que votre compte n’est pas encore vérifié, veuillez vérifier votre badge."
        )

    verification_form = ProfileCompleteForm(instance=user)
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        verification_form = ProfileCompleteForm(
            request.POST,
            instance=user
        )
        user_form = UpdateUserForm(request.POST, instance=user)
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

            if user_form.is_valid():
                user_form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                'Profil modifié avec succès.'
            )
            return redirect('profile_complete')

        else:
            if verification_form.is_valid():
                verification_form.instance.approval_status = 'p'
                # approval status get's pending
                if verification_form.instance.role == verification_form.instance.requested_role:
                    verification_form.instance.approval_status = 'a'
                # but if request_role is for the same role approval status get's accept
                verification_form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Votre demande a été envoyée, veuillez patienter.'
                )
                return redirect('profile_complete')

    user_permissions = user.user_permissions.all()
    ctx.update({
        'verification_form': verification_form,
        'user_form': user_form,
        'user_perms': user_permissions if user_permissions else None,
    })
    return render(request, 'account/profile_complete.html', ctx)


@user_passes_test(user_is_admin_or_su, login_url='permission_error')
def profile_picture_upload(request):
    """
    Handles profile pic uploads coming through ajax.
    """
    if request.method == 'POST':
        image = request.FILES.get('profile-picture')
        try:
            request.user.profile.profile_picture = image
            request.user.profile.save()
            return JsonResponse({
                'status': 'ok',
                'imgUrl': request.user.profile.profile_picture.url,
            })
        except:
            return JsonResponse({'status': 'error'})


# #################################### REQUESTS #################################
class UserRequestsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = User.objects.exclude(approval_status='a')
    template_name = 'account/dashboard/requests/user_requests.html'
    context_object_name = 'users'

    def test_func(self):
        user = self.request.user
        return user_is_admin_or_su(user)


@user_passes_test(user_is_admin_or_su, login_url='permission_error')
def user_approval(request, pk, approved):
    """ Approve or decline approval request based on parameter `approved`.
    approved=0 means decline, 1 means approve.
    """
    user = User.objects.get(pk=pk)
    requested_role = user.requested_role

    if approved:
        assign_role(user, requested_role)
        user.role = requested_role
        if requested_role == 'admin':
            user.is_staff = True
        user.approval_status = 'a'
        user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'le compte de {user} a été approuvé'
        )
    else:
        user.approval_status = 'd'
        user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'La demande de {user} pour le rôle de {requested_role} a été rejeté'
        )
    return redirect('/dashboard/requests')


@user_passes_test(user_is_admin_or_su, login_url='permission_error')
def user_approval_with_modification(request, pk):
    user = User.objects.get(pk=pk)
    form = ApprovalProfileUpdateForm()
    if request.method == 'POST':
        requested_role = request.POST.get('requested_role')
        assign_role(user, requested_role)
        user.role = requested_role
        if requested_role == 'admin':
            user.is_staff = True
        user.approval_status = 'a'
        user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'Le compte de {user}\a été approuvé'
        )
        return redirect('/dashboard/requests')
    ctx = {
        'form': form,
    }
    return render(request, 'account/dashboard/requests/modify_approval.html', ctx)


# ############################# ACCOUNTS #############################
class AccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'account/dashboard/account_list.html'
    context_object_name = 'accounts'

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = UserChangeFormDashboard
    queryset = User.objects.all()
    template_name = 'account/dashboard/account_form.html'
    success_url = reverse_lazy('read_accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = UserChangeFormDashboard
    queryset = User.objects.all()
    template_name = 'account/dashboard/account_form.html'
    success_url = reverse_lazy('read_accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/profile_complete.html'
    success_message = "Mot de passe changé avec succès"
    success_url = reverse_lazy('profile_complete')


class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomGroup
    template_name = 'academic/group_list.html'
    context_object_name = 'groups'

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')
