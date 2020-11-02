from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return "{des}".format(des=self.description)

class Bid(models.Model):
    bidValue = models.FloatField(blank=True,null=True)
    bidOwner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bid_owner")
    date = models.DateTimeField(default=timezone.now)

class Comments(models.Model):
    description = models.CharField(max_length=200)
    commented_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comment_owner")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{des}, {owner}, {date}".format(title=self.title, des=self.description, owner=self.commented_by.username, date=self.date)

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    bidStart = models.FloatField()
    currentBid = models.ForeignKey(Bid, on_delete=models.PROTECT, related_name="bid_listing", null=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listing_owner")
    created_date = models.DateTimeField(default=timezone.now)
    watchers = models.ManyToManyField(User, related_name="watchers")
    status = models.CharField(max_length=50, default=True)
    comments = models.ManyToManyField(Comments ,related_name="listing_comment")

    def __str__(self):
        return "{title}, {des}, {bidStart}".format(title=self.title, des=self.description,  bidStart=self.bidStart)