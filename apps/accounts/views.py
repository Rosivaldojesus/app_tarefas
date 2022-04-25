from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .models import UserProfile
from .forms import UserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def add_user(request):
    template_name = 'accounts/add_user.html'
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.set_password(obj.password)
            obj.save()
            messages.success(request, 'Usuário cadastrado com sucesso')
    form = UserForm()
    context['form'] = form
    return render(request, template_name, context)



def user_login(request):
    template_name = 'accounts/user_login.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/')) # Caputurando a ultima pagina que vou realizado a tenativa de acesso
        else:
            messages.error(request, 'Usuário ou senha inválida.')

    return render(request, template_name, {})


@login_required(login_url='/contas/login/')
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


@login_required(login_url='/contas/login/')
def user_change_password(request):
    template_name = 'accounts/user_change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('/contas/alterar-senha/')
        else:
            messages.error(request, 'Não possível alterar a senha.')
    form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def add_user_profile(request):
    template_name = 'accounts/add_user_profile.html'
    context = {}
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj = form.save()
            obj.save()
            messages.success(request, 'Perfil alterado com sucesso.')
    form = UserProfileForm()
    context['form'] = form
    return render(request, template_name, context)


def list_user_profile(request):
    template_name ='accounts/list_user_profile.html'
    
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        'profile': profile
        
    }
    return render(request, template_name, context )
