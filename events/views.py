from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from common.forms import CommentForm
from common.models import Comment
from events.forms import EventForm
from events.models import Event



class EventListView(ListView):
    model = Event
    template_name = 'events/event-list.html'
    context_object_name = 'events'
    ordering = ['-date']
    paginate_by = 5

    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(date__gte=now).order_by('date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(Event)
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
            return redirect('event-details', pk=self.object.pk)

        # If the form is nort valid, return back with old values
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-add.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            form.add_error(None, "You must be logged in to create an event.")
            return self.form_invalid(form)
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        print("✅ The event was created:", form.instance)
        return response

    def form_invalid(self, form):
        print("⛔ Format errors:", form.errors)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-edit.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        return self.request.user == self.get_object().created_by

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event-delete.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        return self.request.user == self.get_object().created_by
