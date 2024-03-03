from celery import shared_task
import requests
from bs4 import BeautifulSoup
import os
import datetime
from google.oauth2 import service_account
from google.cloud import vision
from API.models import Image
import json

credentials = service_account.Credentials.from_service_account_file(
    '../../uarec-congestion-af000c8e2ed3.json')

@shared_task(bind=True)
def scrape_webcams(self):
    url = "https://rec.arizona.edu/facilities/webcams"
    workingCams = {"Webcam still image of the South Gym facility": "TrainingImages/SouthGym"}
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')

    client = vision.ImageAnnotatorClient(credentials=credentials)

    for image in images:
        if image['alt'] in workingCams:
            name = image['alt']
            link = image['src']
            folder_path = "Temp-Image"
            os.makedirs(folder_path, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = os.path.join(folder_path, name.replace(" ", "_") + '_')
            with open(filename + timestamp + '.jpg', 'wb') as f:
                imgrequest = requests.get(link)
                f.write(imgrequest.content)
            
            with open(filename + timestamp + '.jpg', 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.label_detection(image=image)
            print(response)
            peopleCount = sum(label.description.lower() == 'person' for label in response.label_annotations)

            imageRecord = Image(count=peopleCount, location=(workingCams[name])[15:])
            imageRecord.save()

            os.remove(filename + timestamp + '.jpg')

    return