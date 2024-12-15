import keras_ocr
import os
import matplotlib.pyplot as plt

# Base directory and image path setup
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#IMAGE_PATH = os.path.join(BASE_DIR)
#image_path = os.path.join(IMAGE_PATH, 'Scan_Model', 'idfront (1).jpg')

#print(f"Checking image existence at: {image_path}")
# Initialize keras-ocr pipeline
pipeline = keras_ocr.pipeline.Pipeline()

def detect(image_path):   
        if os.path.isfile(image_path):
            print("Image exists!")
        else:
            print("Image does not exist.")
        
        # Read the image
        image = keras_ocr.tools.read(image_path)

        # Detect text
        prediction_groups = pipeline.recognize([image])

        # Extract detected text
        detected_texts = [text for text, box in prediction_groups[0]]

        # Initialize fields
        course = None
        student_id = None

        # Define contextual keywords for filtering
        course_keywords = ["bsit", "bscs", "bsed", "bsa","bshm", "bstm", "bsentrep", "bspolsci", "bscrim", "bscpe", "bsfi", "beed", "bsed"]  # Common course codes
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
            print(f"Student ID Number: {student_id}")
        else:
            print("Some information could not be detected.")

        # Optionally, display the image with detected text
        #fig, ax = plt.subplots(figsize=(10, 10))
        #ax.imshow(image)
        #for text, box in prediction_groups[0]:
            #ax.add_patch(plt.Polygon(box, fill=False, color='red', linewidth=2))
            #ax.text(box[0][0], box[0][1], text, fontsize=12, color='red', weight='bold')
        #plt.show()

