from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView, UpdateView

from accounts.forms import UserEditForm
from artwork.models import Artwork

UserModel = get_user_model()

class RegisterView(views.CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register_page.html'
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