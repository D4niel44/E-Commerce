from django.db import models
from django.forms import ModelForm

from .models import Listing


class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'initial_bid_amount', 'image', 'category'
        ]
