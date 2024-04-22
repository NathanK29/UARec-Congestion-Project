import requests

class Request:

    url = 'http://50.18.145.8:8000/images/'
    images = None

    def fetch(self):
        
        response = requests.get(self.url)

        if response.status_code == 200:
            data = response.json()
            self.images = data['images']
        else:
            print(f'Request failed with status code: {response.status_code}')


