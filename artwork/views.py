from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from artwork.forms import ArtworkForm
from artwork.models import Artwork
from common.forms import CommentForm
from common.models import Comment


class ArtworkListView(ListView):
    model = Artwork
    template_name = 'artwork/artwork-list.html'
    context_object_name = 'artworks'

class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'artwork/artwork-details.html'
    context_object_name = 'artwork'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(Artwork)
        comments = Comment.objects.filter(
            content_type=content_type,
            object_id=self.object.id
        ).order_by('-created_at')

        context['comments'] = comments
        context['comment_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_object = self.object
            comment.save()
            return redirect('artwork-details', pk=self.object.pk)

        # If the form is nort valid, return back with old values
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


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