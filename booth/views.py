from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.files.base import ContentFile
import io

from .models import Photo
from .serializers import PhotoSerializer
from utils.filters import (
    apply_grayscale,
    apply_sepia,
    apply_blur,
    apply_cartoon,
)


# Upload photo via form
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


# Apply filter to a photo
@api_view(["POST"])
def apply_filter(request, photo_id):
    """
    Apply a filter to an existing photo
    POST body: {"filter": "grayscale"}
    """
    filter_type = request.data.get("filter")  # Changed from GET to data
    
    if not filter_type:
        return Response(
            {"error": "Filter type is required in request body"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        photo = Photo.objects.get(id=photo_id)
    except Photo.DoesNotExist:
        return Response(
            {"error": "Photo not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    image_path = photo.image.path

    # Apply the requested filter
    try:
        if filter_type == "grayscale":
            new_image = apply_grayscale(image_path)
        elif filter_type == "sepia":
            new_image = apply_sepia(image_path)
        elif filter_type == "blur":
            new_image = apply_blur(image_path)
        elif filter_type == "cartoon":
            new_image = apply_cartoon(image_path)
        else:
            return Response(
                {"error": "Invalid filter. Options: grayscale, sepia, blur, cartoon"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save filtered image to BytesIO
        img_io = io.BytesIO()
        new_image.save(img_io, format="JPEG")
        img_content = ContentFile(img_io.getvalue())

        # Save to the filtered_image field
        photo.filtered_image.save(
            f"filtered_{filter_type}_{photo.id}.jpg",
            img_content,
            save=True
        )

        return Response({
            "message": f"{filter_type} filter applied successfully",
            "original_image": request.build_absolute_uri(photo.image.url),
            "filtered_image": request.build_absolute_uri(photo.filtered_image.url)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Filter processing failed: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )