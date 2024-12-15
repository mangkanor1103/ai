from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import keras_ocr
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Function-based view for text detection
@api_view(['POST'])
def detect_text(request):
    # Get the image from the request
    image = request.FILES.get('image')  # Assuming the image is sent in the 'image' field

    if not image:
        return JsonResponse({'error': 'No image provided'}, status=400)

    # Save the image temporarily
    image_path = os.path.join('uploads', image.name)
    with open(image_path, 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)

    # Run keras-ocr
    pipeline = keras_ocr.pipeline.Pipeline()
    image_data = keras_ocr.tools.read(image_path)
    prediction_groups = pipeline.recognize([image_data])

    # Extract the detected text (not returned in the response)
    detected_texts = [text for text, box in prediction_groups[0]]

    # Clean up the temporary image file
    os.remove(image_path)

    # You can return just the extracted information (like course or student_id) without showing the raw text
    return JsonResponse({'message': 'Text extraction completed successfully.'})

# Class-based view for OCR processing with filtering
class OCRView(APIView):

    def post(self, request):
        # Get the uploaded image file from the request
        image_file = request.FILES.get('image')

        if image_file:
            # Save the image temporarily
            image_path = os.path.join('tmp', image_file.name)
            with open(image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # Initialize keras-ocr pipeline
            pipeline = keras_ocr.pipeline.Pipeline()

            # Read the image
            image = keras_ocr.tools.read(image_path)

            # Detect text
            prediction_groups = pipeline.recognize([image])

            # Extract detected text (not returned in the response)
            detected_texts = [text for text, box in prediction_groups[0]]

            # Define contextual keywords for filtering
            course_keywords = ["bsit", "bscs", "bsed", "bsa", "bshm", "bstm", "bsentrep", "bspolsci", "bscrim", "bscpe", "bsfi", "beed", "bsed"]
            id_prefix = "mbc"  # Adjust based on your ID prefix
            excluded_keywords = ["student", "card", "identification", "university", "state", "mindoro", "issued", "number", "stupent", "phd", "president", "campus", "main"]

            course = None
            student_id = None

            # Loop through detected texts and filter based on keywords
            for text in detected_texts:
                if id_prefix in text.lower() and any(char.isdigit() for char in text):
                    student_id = text.upper()  # Save the student ID
                elif any(course_keyword in text.lower() for course_keyword in course_keywords):
                    course = text.upper()  # Save the detected course

            return Response({
                'course': course,
                'student_id': student_id
            }, status=status.HTTP_200_OK)

        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
