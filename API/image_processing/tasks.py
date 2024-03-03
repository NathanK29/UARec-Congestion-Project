from celery import shared_task
import requests
from bs4 import BeautifulSoup
import os
import datetime

@shared_task(bind=True)
def scrape_webcams(self):
    url = "https://rec.arizona.edu/facilities/webcams"
    workingCams = {"Webcam still image of the South Gym facility": "TrainingImages/SouthGym"}
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')

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
    return "Done"