import keras_ocr
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(BASE_DIR, 'VOTING_DJANGO')

image_path = os.path.join(IMAGE_PATH,'idfront (1).jpg' )


# Initialize keras-ocr pipeline
pipeline = keras_ocr.pipeline.Pipeline()

# Load your image
image = keras_ocr.tools.read(image_path)



# Perform text detection
prediction_groups = pipeline.recognize([image])

# Extract detected text
detected_texts = [text for text, box in prediction_groups[0]]

# Initialize fields
course = None
student_id = None

# Define contextual keywords for filtering
course_keywords = ["bsit", "bscs", "bsed", "bsa"]  # Common course codes
id_prefix = "mbc"  # Adjust based on your ID prefix
excluded_keywords = ["student", "card", "identification", "university", "state", "mindoro", "issued", "number", "stupent", "phd", "president", "campus", "main"]
 
# Logic for extracting fields
for text in detected_texts:
    # Identify Student ID (matches prefix and contains numbers)
    if id_prefix in text.lower() and any(char.isdigit() for char in text):
        student_id = text.upper()

    # Identify Course (matches predefined course keywords)
    elif any(course_keyword in text.lower() for course_keyword in course_keywords):
        course = text.upper()

# Output extracted details
if course and student_id:
    print(f"Course: {course}")
    print(f"Student Id Number: {student_id}")
else:
    print("Some information could not be detected.")
