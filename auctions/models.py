from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing',
                                       blank=True,
                                       related_name='users_watching')


# TODO validate money fields
class Listing(models.Model):
    user = models.ForeignKey('User',
                             on_delete=models.PROTECT,
                             related_name='listings')
    status = models.ForeignKey('Status',
                               on_delete=models.PROTECT,
                               related_name='listings')
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to=f'{title}', blank=True, null=True)
    initial_bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    actual_bid = models.OneToOneField('Bid',
                                      on_delete=models.PROTECT,
                                      blank=True,
                                      null=True,
                                      related_name='listing_active_bid')
    category = models.ForeignKey('Category', on_delete=models.PROTECT)


class Bid(models.Model):
    user = models.ForeignKey('User',
                             on_delete=models.PROTECT,
                             related_name='bids')
    listing = models.ForeignKey('Listing',
                                on_delete=models.CASCADE,
                                related_name='bids')
    amount = models.DecimalField(max_digits=12, decimal_places=2)


class Comment(models.Model):
    user = models.ForeignKey('User',
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='comments')
    listing = models.ForeignKey('Listing',
                                on_delete=models.CASCADE,
                                related_name='comments')
    text = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=9)
    can_bid = models.BooleanField()

    def __str__(self):
        return self.name
