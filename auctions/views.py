from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Status
from .forms import CreateListingForm, BidForm


def index(request):
    return render(
        request,
        "auctions/index.html",
        {
            "listings": Listing.objects.filter(status=1),
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html",
                      {"message": "Invalid username and/or password."})
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html",
                          {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html",
                          {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    template = 'auctions/create_listing.html'
    if request.method == 'POST':
        user = request.user
        status = Status.objects.get(name='Active')
        incomplete_listing = Listing(user=user, status=status)
        form = CreateListingForm(request.POST, instance=incomplete_listing)
        if form.is_valid():
            listing = form.save()
            return HttpResponseRedirect(reverse('listing', args=[listing.pk]))
        return render(request, template, {
            'form': form,
        })
    return render(request, template, {
        'form': CreateListingForm(),
    })


def listing(request, listing_id):
    template = 'auctions/listing.html'
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if request.method == 'POST':
        incomplete_bid = Bid(user=user, listing=listing)
        form = BidForm(request.POST, instance=incomplete_bid)
        if form.is_valid():
            listing = form.save().listing
            return HttpResponseRedirect(reverse('listing', args=[listing.pk]))
        return render(
            request, template, {
                'form': form,
                'listing': listing,
                'comments': listing.comments.all(),
                'bids_count': listing.bids.count(),
                'has_bid': listing.bids.filter(user=user).count(),
            })
    return render(
        request, 'auctions/listing.html', {
            'form': BidForm(),
            'listing': listing,
            'comments': listing.comments.all(),
            'bids_count': listing.bids.count(),
            'has_bid': listing.bids.filter(user=user).count(),
        })
