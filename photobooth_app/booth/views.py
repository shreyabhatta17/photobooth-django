from django.shortcuts import render
from django.http import JsonResponse
from .models import Photo
from rest_framework import generics
from .serializers import PhotoSerializer

def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('image'):
        photo = Photo.objects.create(image=request.FILES['image'])
        return JsonResponse({'message': 'Uploaded', 'image_url': photo.image.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# List all photos + upload new one
class PhotoListCreateView(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

# Fetch a single photo
class PhotoDetailView(generics.RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer