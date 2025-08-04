from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView, UpdateView

from accounts.forms import UserEditForm, UserRegistrationForm, CustomLoginForm
from artwork.models import Artwork

UserModel = get_user_model()

class RegisterView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('login')

class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context["artworks"] = Artwork.objects.filter(owner=user)
        return context

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    form_class = UserEditForm
    template_name = 'accounts/profile-edit-page.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

def app_user_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = UserModel.objects.get(pk=pk)

    if request.user.is_authenticated and request.user.pk == user.pk:
        if request.method == 'POST':
            user.delete()
            return redirect('home')
    else:
        return HttpResponseForbidden()

    return render(request, 'accounts/profile-delete-page.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or where you want to redirect after registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register-page.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    authentication_form = CustomLoginForm

