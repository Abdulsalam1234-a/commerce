from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    author = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(max_length=255, null=True, blank=True)
    date = models.DateField(blank=True, null=True, default=datetime.now)

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listing_owner")
    start_bid = models.FloatField()
    last_bid = models.FloatField(blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, blank=True, null=True, related_name="listing_category")
    is_active = models.BooleanField(default=1)
    watchlist = models.ManyToManyField("User", blank=True, null=True, related_name="watchlist_listing")
    
    def __str__(self):
        return f"{self.title} {self.owner} {self.category} {self.start_bid}"
    

class Bid(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, blank=True, null=True, related_name="bid_listing")
    bidder = models.CharField(max_length=50, null=True, blank=True)
    bid = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.listing} {self.bid}"
    

class Watchlist(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name="watchlist_user")
    list_item = models.ManyToManyField("Listing", blank=True, null=True, related_name="list_item_watchlist")
    
    def __str__(self):
        return f"{self.user} {self.list_item}"