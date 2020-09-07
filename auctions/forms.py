from django.db import models
from django.forms import ModelForm, Textarea

from .models import Listing, Bid, Comment


def add_class(fields):
    for field in fields.values():
        field.widget.attrs.update({'class': 'form-control'})


class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'initial_bid_amount', 'image_URL', 'category'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class(self.fields)


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = [
            'amount',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class(self.fields)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['text'].widget = Textarea()
        add_class(self.fields)
