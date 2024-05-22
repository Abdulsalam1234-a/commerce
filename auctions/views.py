from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Comment, Listing, Watchlist, Category, Bid
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import CreateListingForm, CommentForm, BidForm


def index(request):
    activeListing = Listing.objects.filter(is_active=True)
    # categories = Category.objects.all()
    
    # if request.method == "POST":
    #     catData = request.POST["categories"]
    #     cat_match = Category.objects.get(name=catData)
        
    #     return HttpResponseRedirect(reverse("category", args=[cat_match.id]))
    
    return render(request, "auctions/index.html", {
        "activeListing": activeListing,
        # "categories": categories
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

@login_required(login_url="login")
def create_listing(request):
    form = CreateListingForm()
    
    if request.method == "POST":
        listData = CreateListingForm(request.POST)
        
        if listData.is_valid():
            obj = listData.save(commit=False)
            obj.owner = User.objects.get(pk=request.user.id)
            obj.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createlisting.html", {
                "message": "Error creating lisst item",
                "form": form
        })
    return render(request, "auctions/createlisting.html", {
        "form": form
    })
    
def close_listing(request, id):
    listItem = Listing.objects.get(pk=id)
    listItem.is_active = False
    listItem.save()
        
    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required(login_url="login")
def listing(request, id):
    listItem = Listing.objects.get(id=id)
    user = User.objects.get(pk=request.user.id)
    comments = Comment.objects.filter(listing=listItem)
    owner = None
    if user == listItem.owner:
        owner = True
    bidError = None
    if "bidError" in request.session:
        bidError = request.session["bidError"]
        
    is_in_watchlist =request.user in listItem.watchlist.all()
    return render(request, "auctions/listing.html", {
        "listItem": listItem,
        "owner": owner,
        "commentForm": CommentForm(),
        "bidForm": BidForm(),
        "comments": comments,
        "bidError": bidError,
        "is_in_watchlist": is_in_watchlist
    })
    
    
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, name):
    category_listings = Listing.objects.filter(category=name)
    title = Category.objects.get(id=name)
    
    
    return render(request, "auctions/category.html", {
        "category_listings": category_listings,
        "name": title.name
    })
    
def comment(request, list_id):
    listItem = Listing.objects.get(id=list_id)
    
    if request.method == "POST":
        commentText = CommentForm(request.POST)
        if commentText.is_valid():
            obj = commentText.save(commit=False)
            obj.author = User.objects.get(pk=request.user.id)
            obj.listing = listItem
            obj.save()
            
            return HttpResponseRedirect(reverse("listing", args=[list_id]))

def bid(request, list_id):
    listItem = Listing.objects.get(id=list_id)
    lastBid = listItem.last_bid
    
    if lastBid is None:
        lastBid = listItem.start_bid
    currentPrice = lastBid
    
    if request.method == "POST":
        bid_price = BidForm(request.POST)
        if bid_price.is_valid():
            bid_new_price = bid_price.cleaned_data["bid"]
            if bid_new_price is None:
                bid_new_price = 0
            if bid_new_price <= currentPrice:
                request.session["bidError"] = "Error: Could not place bid, bid is lower or equal to start bid / current-last bid"
                return (HttpResponseRedirect(reverse("listing", args=[list_id])))
            try:
                del request.session["bidError"]
            except:
                pass
            obj = bid_price.save(commit=False)
            obj.author = User.objects.get(pk=request.user.id)
            obj.listing = listItem
            obj.save()
            listItem.last_bid = bid_new_price
            listItem.save()
            
            return HttpResponseRedirect(reverse("listing", args=[list_id]))
    try:
        del request.session["bidError"]
    except:
        pass
    return HttpResponseRedirect(reverse("listing", args=[list_id]))

    
def watchlists(request):
    user = request.user
    watchlistItems = user.watchlist_listing.all()
    return render(request, "auctions/watchlist.html", {
        "watchlistItems": watchlistItems
    })
    
def addWatchlist(request, id):
    listItem = Listing.objects.get(pk=id)
    currentUser = request.user
    listItem.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=[id,]))

def removeWatchlist(request, id):
    listItem = Listing.objects.get(pk=id)
    currentUser = request.user
    listItem.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=[id,]))