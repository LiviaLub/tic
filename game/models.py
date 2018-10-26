from django.db import models

# Create your models here.


# Create your models here.


class Game(models.Model):

    game_number = models.IntegerField()
    winner = models.CharField(max_length=1, null=True)

class Move(models.Model):

    player = models.CharField(max_length=1)
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
