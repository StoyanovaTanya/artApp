from django.urls import path
from artwork import views

urlpatterns = [
    path('', views.ArtworkListView.as_view(), name='artwork-list'),
    path('create/', views.ArtworkCreateView.as_view(), name='artwork-create'),
    path('<int:pk>/', views.ArtworkDetailView.as_view(), name='artwork-details'),
    path('<int:pk>/edit/', views.ArtworkUpdateView.as_view(), name='artwork-edit'),
    path('<int:pk>/delete/', views.ArtworkDeleteView.as_view(), name='artwork-delete'),
]