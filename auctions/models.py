from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from decimal import Decimal


# Validator for a Decimal field representing a price
def positive_decimal_field(decimal_field):
    if decimal_field.compare(Decimal(0)) <= 0:
        raise ValidationError('Only positive values allowed for prices')


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing',
                                       blank=True,
                                       related_name='users_watching')


class Listing(models.Model):
    user = models.ForeignKey('User',
                             on_delete=models.PROTECT,
                             related_name='listings')
    status = models.ForeignKey('Status',
                               on_delete=models.PROTECT,
                               related_name='listings')
    title = models.CharField(max_length=24)
    description = models.TextField(max_length=512)
    image_URL = models.URLField(blank=True, null=True)
    initial_bid_amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[positive_decimal_field])
    actual_bid = models.OneToOneField('Bid',
                                      on_delete=models.PROTECT,
                                      blank=True,
                                      null=True,
                                      related_name='listing_active_bid')
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 related_name='listings')


class Bid(models.Model):
    user = models.ForeignKey('User',
                             on_delete=models.PROTECT,
                             related_name='bids')
    listing = models.ForeignKey('Listing',
                                on_delete=models.CASCADE,
                                related_name='bids')
    amount = models.DecimalField(max_digits=12,
                                 decimal_places=2,
                                 validators=[positive_decimal_field])

    def clean(self):
        listing = self.listing
        # If there is no amount at his point then amount fields validations failed
        if not self.amount:
            return
        if not listing.status.can_bid:
            raise ValidationError('This listing is no longer open')
        if self.user == listing.user:
            raise ValidationError(
                'You are not allowed to bid on self listings')
        condition_1 = listing.actual_bid and self.amount.compare(
            listing.actual_bid.amount) <= 0
        condition_2 = self.amount.compare(listing.initial_bid_amount) < 0
        if condition_1 or condition_2:
            raise ValidationError({
                'amount': [
                    'Bid should be greater than actual bid or at least the starting bid price',
                ]
            })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.listing.actual_bid = self
        self.listing.save()


class Comment(models.Model):
    user = models.ForeignKey('User',
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='comments')
    listing = models.ForeignKey('Listing',
                                on_delete=models.CASCADE,
                                related_name='comments')
    text = models.TextField(max_length=256)
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
