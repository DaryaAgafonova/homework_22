from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.conf import settings

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User


class UserRegistrationView(CreateView):

    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # Сохраняем пользователя
        response = super().form_valid(form)
        
        # Авторизуем пользователя
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        
        # Отправляем приветственное письмо
        send_mail(
            'Добро пожаловать в Skystore!',
            f'Здравствуйте, {user.email}!\n\nСпасибо за регистрацию на нашем сайте. '
            f'Теперь вы можете просматривать, создавать и редактировать товары.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return response


class UserLoginView(LoginView):
    
    form_class = UserLoginForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LogoutView):

    next_page = reverse_lazy('home')


@login_required
def profile_view(request):
    
    return render(request, 'users/profile.html', {'user': request.user})


class UserProfileUpdateView(UpdateView):
    
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user