from django.db import models
from django.contrib.auth.models import User
class Movie(models.Model): #define python class
    id = models.AutoField(primary_key=True) #autofield auotmatically increments value for each new record
    name = models.CharField(max_length=255) #string mac length 255 char
    price = models.IntegerField() #integer value
    description = models.TextField() #no specified max length
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reported = models.BooleanField(default=False)
    report = models.CharField(max_length=255, default='') #pop up on screen to write a report about the review
    def __str__(self):
        if self.reported:
            return str(self.id) + ' - ' + self.movie.name + ' REPORTED'
        return str(self.id) + ' - ' + self.movie.name
# each time make changes to a model file, make migrations to it
# python3 manage.py makemigrations
# python3 manage.py migrate