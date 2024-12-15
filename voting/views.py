from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


import os
from django.core.files.storage import default_storage
from Scan_Model import img # Import the detect function from img.py

@api_view(['POST'])
def detect_text(request):
    # Get the image from the request
    image = request.FILES.get('image')

    if not image:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)


    return Response({'message': 'Image received successfully!'}, status=status.HTTP_200_OK)
