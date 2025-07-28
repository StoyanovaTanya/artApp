from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from artwork.forms import ArtworkForm
from artwork.models import Artwork


class ArtworkListView(ListView):
    model = Artwork
    template_name = 'artwork/artwork-list.html'
    context_object_name = 'artworks'

class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'artwork/artwork-details.html'
    context_object_name = 'artwork'

class ArtworkCreateView(LoginRequiredMixin, CreateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artwork/artwork-create.html'
    success_url = reverse_lazy('artwork-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ArtworkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artwork/artwork-edit.html'
    success_url = reverse_lazy('artwork-list')

    def test_func(self):
        artwork = self.get_object()
        return self.request.user == artwork.owner

class ArtworkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Artwork
    template_name = 'artwork/artwork-delete.html'
    success_url = reverse_lazy('artwork-list')

    def test_func(self):
        artwork = self.get_object()
        return self.request.user == artwork.owner