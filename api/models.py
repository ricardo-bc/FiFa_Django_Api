from django.db import models

# Create your models here.

class gamer(models.Model):
    class Meta:
        managed= 'api_gamer'
    name =  models.CharField(max_length=50, default='')
    game_position = models.CharField(max_length=50, default='')
    nationality = models.CharField(max_length=50, default='')
    team = models.CharField(max_length=50, default='')
    def __str__(self):
        return self.name



