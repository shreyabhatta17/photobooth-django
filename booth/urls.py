from django.urls import path
from . import views

urlpatterns = [
    path('photos/', views.PhotoListCreateView.as_view(), name='photo-list'),
    path('photos/<int:pk>/', views.PhotoDetailView.as_view(), name='photo-detail'),
    path('photos/<int:photo_id>/filter/', views.apply_filter, name='apply-filter'),
    path('upload/', views.upload_photo, name='upload-photo'),
]