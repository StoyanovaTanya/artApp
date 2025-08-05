from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from common.forms import CommentForm
from common.models import Comment
from events.forms import EventForm, EventParticipationForm
from events.models import Event, EventParticipationRequest


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

        # --- COMMENTS ---
        content_type = ContentType.objects.get_for_model(Event)
        comments = Comment.objects.filter(
            content_type=content_type,
            object_id=self.object.id
        ).order_by('-created_at')

        context['comments'] = comments
        context['comment_form'] = kwargs.get('comment_form', CommentForm())

        # --- PARTICIPATION ---
        context['participation_form'] = kwargs.get('participation_form', EventParticipationForm())
        context['requests'] = self.object.participation_requests.all()

        return context

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to perform this action.")
            return redirect('login')

        self.object = self.get_object()
        form_type = request.POST.get('form_type')

        # --- Comment form submitted ---
        if form_type == 'comment':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.content_object = self.object
                comment.save()
                messages.success(request, "Your comment has been posted.")
                return redirect('event-details', pk=self.object.pk)
            else:
                # върни page с грешките за коментара
                context = self.get_context_data(comment_form=form, participation_form=EventParticipationForm())
                messages.error(request, "Please correct the comment form errors.")
                return self.render_to_response(context)

        # --- Participation form submitted ---
        elif form_type == 'participation':
            form = EventParticipationForm(request.POST)
            if form.is_valid():
                try:
                    req, created = EventParticipationRequest.objects.get_or_create(
                        event=self.object,
                        user=request.user,
                        defaults={'message': form.cleaned_data.get('message', '')}
                    )
                except Exception as e:
                    messages.error(request, f"Error creating request: {e}")
                    context = self.get_context_data(comment_form=CommentForm(), participation_form=form)
                    return self.render_to_response(context)

                if created:
                    messages.success(request, "Your participation request has been submitted.")
                else:
                    messages.warning(request, "You already submitted a request for this event.")
                return redirect('event-details', pk=self.object.pk)
            else:
                context = self.get_context_data(comment_form=CommentForm(), participation_form=form)
                messages.error(request, "Please correct the participation form errors.")
                return self.render_to_response(context)

        else:
            messages.error(request, "Invalid form submission.")
            return redirect('event-details', pk=self.get_object().pk)

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

@login_required
def approve_request(request, event_pk, req_pk):
    # само POST допускаме
    if request.method != 'POST':
        return HttpResponseForbidden()

    event = get_object_or_404(Event, pk=event_pk)
    # само организаторът или суперюзер може да одобрява
    if request.user != event.created_by and not request.user.is_superuser:
        return HttpResponseForbidden()

    req = get_object_or_404(EventParticipationRequest, pk=req_pk, event=event)
    req.status = 'approved'
    req.save()

    messages.success(request, f"Request from {req.user.username} approved.")
    return redirect('event-details', pk=event_pk)


@login_required
def reject_request(request, event_pk, req_pk):
    if request.method != 'POST':
        return HttpResponseForbidden()

    event = get_object_or_404(Event, pk=event_pk)
    if request.user != event.created_by and not request.user.is_superuser:
        return HttpResponseForbidden()

    req = get_object_or_404(EventParticipationRequest, pk=req_pk, event=event)
    req.status = 'rejected'
    req.save()

    messages.info(request, f"Request from {req.user.username} rejected.")
    return redirect('event-details', pk=event_pk)