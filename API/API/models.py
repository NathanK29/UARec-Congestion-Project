from django.db import models

class Image(models.Model):
    count = models.IntegerField()
    location = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    

    def __str__(self):
        formatted_time = self.time.strftime("%H:%M:%S")
        return f'Image of {self.count} people taken at {formatted_time} on {self.date} at {self.location}'