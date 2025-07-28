from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from events.forms import EventForm
from events.models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/event-list.html'
    context_object_name = 'events'
    ordering = ['-date']
    paginate_by = 5

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-add.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event-edit.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        return self.request.user == self.get_object().created_by

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event-delete.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        return self.request.user == self.get_object().created_by