import os
from pylons import app_globals

def generate_path(image):
    return os.path.join(app_globals.image_storage, image.path)

def delete_image(image):
    path = generate_path(image)
    os.remove(path)

