import requests
import os

valid_images_extensions = ['jpg', 'jpeg', 'png', 'gif']

def download_by_url(image_url, image_path):
    extension = get_extension_from_url(image_url)
    if(extension in valid_images_extensions):
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)

def get_extension_from_url(url):
    return url.split('?')[0].split('.')[-1]

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)