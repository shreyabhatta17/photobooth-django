from django.urls import path
from . import views
from .views import PhotoListCreateView, PhotoDetailView

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photos/', PhotoListCreateView.as_view(), name='photo-list'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
]
