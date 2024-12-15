import keras_ocr
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(BASE_DIR, 'VOTING_DJANGO')

image_path = os.path.join(IMAGE_PATH,'idfront (1).jpg' )

pipeline = keras_ocr.pipeline.Pipeline()

# Read the image
image = keras_ocr.imread(image_path)

# Predict the text
prediction_groups = pipeline.recognize([image])

# Extract the text
for group in prediction_groups:
    for box, text, prob in group:
        print(f'Text: {text}, Probability: {prob:.2f}')