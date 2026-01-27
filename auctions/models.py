from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(blank=True, choices=[('EL', 'Electronics'), ('CL', 'Clothes')])
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}. {self.title}: {self.description} | Starting bid: {self.starting_bid} "
    
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)