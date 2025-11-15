from django.shortcuts import render
from django.http import JsonResponse
from .models import Photo

def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('image'):
        photo = Photo.objects.create(image=request.FILES['image'])
        return JsonResponse({'message': 'Uploaded', 'image_url': photo.image.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)
