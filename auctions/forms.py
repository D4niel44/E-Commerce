from django.db import models
from django.forms import ModelForm

from .models import Listing, Bid, Comment


class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'initial_bid_amount', 'image', 'category'
        ]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = [
            'amount',
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
