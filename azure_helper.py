from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
import json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient 
from msrest.authentication import CognitiveServicesCredentials
from types import SimpleNamespace
from PIL import Image
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
import time

class AzureComputerVisionConnector:

    def __init__(self, base_path, appsettings_file = './appsettings.json', original_folder_name = 'original', json_analysis_folder = 'analysis'):
        self.appsettings_file = appsettings_file
        self.base_path = base_path
        self.original_folder_name = original_folder_name
        self.json_analysis_folder = json_analysis_folder

    def get_client(self) -> ComputerVisionClient:
        appsettings = {}

        with open(self.appsettings_file) as f:
            appsettings = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))

        credentials = CognitiveServicesCredentials(appsettings.azure_key)
        client = ComputerVisionClient(appsettings.azure_endpoint, credentials)
        print(client.api_version)
        return client

    def analyze_all_images(self, filenames, patch_size = 19, time_interval=60):
        predictions = []
        l = len(filenames)
        n_patch = 0
        for i in range(l):
            filename = filenames[i]
            print(f'Analisando imagem ({i}/{l}): {filename}')
            filePath = self.__get_image_original_path(filename)
            image_stream = self.__get_image_stream(filePath)
            analysis_result = self.analyze_image(image_stream)
            self.__save_as_json(analysis_result, filename)
            predictions.append(self.create_prediction_item(analysis_result, filePath))
            self.draw_rectangle(filePath, analysis_result['brands'][0]['rectangle'])

            if(n_patch >= patch_size):
                time.sleep(time_interval)
                n_patch = 0

        return pd.DataFrame(predictions)

    def __get_image_original_path(self, filename):
        return f"{self.base_path}/{self.original_folder_name}/{filename}"

    def __get_image_stream(self, filePath):        
        image = Image.open(filePath)

        png_bytes_io = BytesIO()
        image.save(png_bytes_io, format='JPEG')
        png_bytes_io.seek(0)
        return png_bytes_io

    def get_brands(self, analise):
        brands = []
        for brand in analise.brands:
            brands.append({
                'name': brand.name,
                'confidence': brand.confidence,
                'rectangle': {
                    'x': brand.rectangle.x,
                    'y': brand.rectangle.y,
                    'w': brand.rectangle.w,
                    'h': brand.rectangle.h
                }
            })        
        return brands

    def get_tags(self, analysis):
        tags = []
        for tag in analysis.tags:
            tags.append({
                'name': tag.name,
                'confidence': tag.confidence
            })
        return tags

    def get_caption(self, analysis):
        captions = []    
        for c in analysis.description.captions:
            captions.append({
                'text': c.text,
                'confidence': c.confidence
            })
        return captions

    def analyze_image(self, client, image):
        analysis = client.analyze_image_in_stream(image, visual_features=[VisualFeatureTypes.brands, VisualFeatureTypes.tags, VisualFeatureTypes.description, VisualFeatureTypes.objects])
        brands = self.get_brands(analysis)
        tags = self.get_tags(analysis)
        captions = self.get_caption(analysis)    
        return {
            'brands': brands,
            'tags': tags,
            'captions': captions
        }

    def __save_as_json(self, analysis_result, filename) -> str:
        filePath = f"{self.base_path}/{self.json_analysis_folder}/{filename.split('.')[0]}.json"
        with open(filePath, 'w') as f:
            json.dump(analysis_result, f)
        return filePath

    def create_prediction_item(self, analysis_result, filename):
        brand = ''
        if(len(analysis_result['brands']) > 0):
            brand = analysis_result['brands'][0]['name']

        caption = ''
        if(len(analysis_result['captions']) > 0):
            caption = analysis_result['captions'][0]['text']

        return {
                'filename': filename,
                'brand': brand,
                'caption': caption
            }

    def draw_rectangle(self, filePath, rectangle):
        img = matplotlib.image.imread(filePath)
        img.na
        figure, ax = plt.subplots(1)
        rect = matplotlib.patches.Rectangle((rectangle['x'], rectangle['y']), rectangle['w'], rectangle['h'], fill=False, edgecolor='red', linewidth=2)
        ax.imshow(img)
        ax.add_patch(rect)
        directory = 'data/marked_images/'        
        plt.savefig(filePath)