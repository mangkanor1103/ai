from img import detect
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(BASE_DIR)
image_path = os.path.join(IMAGE_PATH, 'Scan_Model', 'idfront (1).jpg')

detect(image_path)