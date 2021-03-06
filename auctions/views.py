from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Status, Comment, Category
from .forms import CreateListingForm, BidForm, CommentForm


def index(request):
    return render(
        request,
        'auctions/index.html',
        {
            'title': 'Active Listings',
            'listings': Listing.objects.filter(status=1),
        },
    )


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'auctions/login.html',
                      {'message': 'Invalid username and/or password.'})
    return render(request, 'auctions/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        # Ensure all fields are filled
        if not (username and email and password):
            return render(request, 'auctions/register.html',
                          {'message': 'All fields must be filled'})

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, 'auctions/register.html',
                          {'message': 'Passwords must match.'})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'auctions/register.html',
                          {'message': 'Username already taken.'})
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/register.html')


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
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        return render(request, template, {
            'form': form,
        })
    return render(request, template, {
        'form': CreateListingForm(),
    })


def listing(request, listing_id):
    template = 'auctions/listing.html'
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    basic_template_parameters = {
        'form': BidForm(),
        'comment_form': CommentForm(),
        'listing': listing,
        'comments': listing.comments.all(),
        'bids_count': listing.bids.count(),
        'has_bid': False,
        'is_on_watchlist': False,
    }
    if user.is_authenticated and request.method == 'POST':
        incomplete_bid = Bid(user=user, listing=listing)
        form = BidForm(request.POST, instance=incomplete_bid)
        if form.is_valid():
            listing = form.save().listing
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        basic_template_parameters['form'] = form
    if user.is_authenticated:
        basic_template_parameters['has_bid'] = listing.bids.filter(
            user=user).exists()
        basic_template_parameters[
            'is_on_watchlist'] = listing.users_watching.filter(
                id=user.id).exists()
    return render(request, 'auctions/listing.html', basic_template_parameters)


@login_required
def toogle_watchlist(request, listing_id):
    if request.method == 'POST':
        user = request.user
        listing = Listing.objects.get(id=listing_id)
        if listing.users_watching.filter(id=user.id).exists():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
        user.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required
def close_listing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        if request.user == listing.user and listing.status.can_bid:
            if listing.actual_bid:
                listing.status = Status.objects.get(name='Sold')
            else:
                listing.status = Status.objects.get(name='Cancelled')
            listing.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required
def post_comment(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        base_comment = Comment(user=request.user, listing=listing)
        form = CommentForm(request.POST, instance=base_comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required
def watchlist(request):
    user = request.user
    return render(request, 'auctions/index.html', {
        'title': 'Listings on Watchlist',
        'listings': user.watchlist.all(),
    })


def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories': Category.objects.all(),
    })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'auctions/index.html', {
        'title': category.name,
        'listings': category.listings.all(),
    })
