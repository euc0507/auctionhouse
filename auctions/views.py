from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

from django import forms

from .models import User, Listing, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ["creator", "active_flag"]

def create(request):
    form = NewListing()
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return redirect('index')

    return render(request, "auctions/create.html",{
        "form": form
    })


class NewBid(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ["bidder","listing"]

def listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    highest_bid = listing.bid_set.order_by('-amount').first()
    low_bid = False
    if request.method == "POST":
        if request.user == listing.creator:
            listing.active_flag = False
            if highest_bid:
                listing.winner = highest_bid.bidder
                listing.save()

        if request.user.is_authenticated:
            form = NewBid(request.POST)
            if form.is_valid() and listing.active_flag:
                bid = form.save(commit=False)
                bid.bidder = request.user
                bid.listing = listing
                if highest_bid:
                    current_price = highest_bid.amount
                else:
                    current_price = bid.listing.starting_bid

                if bid.amount > current_price:
                    bid.save()
                    return redirect("listing", id=id)
                else:
                    low_bid = "Your bid must be higher than the current bid."

    form = NewBid()
    if highest_bid:
        current_price = highest_bid.amount
    else:
        current_price = listing.starting_bid
    return render(request, "auctions/listing.html",{
        "id": id,
        "listing": listing,
        "category": listing.get_category_display(),
        "form": form,
        "current_price": current_price,
        "highest_bid": highest_bid,
        "low_bid": low_bid
    })


