from events import views
from django.urls import path, include



urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('create/', views.EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/', include([
        path('',views.EventDetailView.as_view(), name='event-details'),
        path('edit/', views.EventUpdateView.as_view(), name='event-edit'),
        path('delete/', views.EventDeleteView.as_view(), name='event-delete'),
    ])),
    path('<int:event_pk>/approve-request/<int:req_pk>/', views.approve_request, name='approve-request'),
    path('<int:event_pk>/reject-request/<int:req_pk>/', views.reject_request, name='reject-request'),
]