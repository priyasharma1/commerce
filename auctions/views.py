import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from django.forms import ModelForm,  modelformset_factory
from .models import User, Listing, Category, Bid, Comments


def index(request):
    return render(request, "auctions/index.html")

class newListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'bidStart', 'category', 'url']

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

def new_listing(request):
        return render(request, "auctions/newListing.html")

def edit_listing(request, id):
    return render(request, "auctions/newListing.html", {
        "listing": Listing.objects.get(id=id)
    })

def create_listing(request):
    if request.method == "POST":
        if request.POST.get('id') is not None:
            newListing = Listing.objects.get(id=request.POST.get('id'))
        else:
            newListing = Listing()
        newListing.title = request.POST.get('title')
        newListing.description = request.POST.get('description')
        newListing.bidStart = request.POST.get('bidStart')
        newListing.category = request.POST.get('category')
        newListing.url = request.POST.get('image')
        newListing.owner = request.user
        newListing.save()
        if newListing.category is not None:
            category = Category.objects.filter(description=newListing.category)
            if not category:
                category = Category()
                category.description = newListing.category
                category.save()
            else:
                print("Category exists with description " + newListing.category)
        return render(request, "auctions/item.html", {
            "listing": newListing
        })
    else:
        return render(request, "auctions/allListings.html", {
            "form": newListingForm(),
        })

def all_listings(request):
    listings = Listing.objects.all()
    return render(request, "auctions/allListings.html", {
        "listings": listings
    })
@csrf_exempt
def listing(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == "POST":
        if request.POST.get("bidValue") is not None:
            return make_bid(request, id)
        elif request.POST.get("status") is not None:
            listing.status = False
            listing.save()
        elif request.POST.get("comment") is not None:
            comment = Comments()
            comment.description = request.POST.get("comment")
            comment.commented_by = request.user
            comment.save()
            listing.comments.add(comment)
            listing.save()
    return render(request, "auctions/item.html", {
        "listing": Listing.objects.get(id=id)
    })

def delete(request, id):
    listing = Listing.objects.get(id=id)
    listing.delete()
    return render(request, "auctions/allListings.html", {
        "listings": Listing.objects.all()
    })

@csrf_exempt
def make_bid(request, id):
    bidValue = int(request.POST.get("bidValue", False))
    listing = Listing.objects.get(id=id)
    bid = listing.currentBid
    if bid is not None:
        if bidValue > listing.bidStart and bidValue > bid.bidValue:
            bid.bidValue = bidValue
        else:
            return render(request, "auctions/item.html", {
                "listing": listing,
                "message": "This bid is invalid."
            })
    else:
        bid = Bid()
        bid.bidValue = bidValue

    bid.bidOwner = request.user
    bid.save()
    listing.currentBid = bid
    listing.save()
    return render(request, "auctions/item.html", {
        "listing": Listing.objects.get(id=id)
    })

@csrf_exempt
def watch(request, id):
    data = json.loads(request.body.decode('utf-8'))
    listing = Listing.objects.get(id=id)
    if data.get("value") == 'Y':
        listing.watchers.add(request.user)
    else:
        listing.watchers.remove(request.user)
    listing.save()
    return render(request, "auctions/item.html", {
        "listing": listing
    })

def watch_list(request):
    listing = Listing.objects.filter(watchers=request.user)
    return render(request, "auctions/allListings.html", {
        "listings": listing
    })

def categories(request):
    categories = Category.objects.all()
    print(str(categories))
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/allListings.html", {
        "listings": listings
    })

@csrf_exempt
def delete_comment(request, id):
    comment = Comments.objects.filter(id=id)
    comment.delete()
    return JsonResponse({
        "message": "Comment deleted"
    }, status=400)


@csrf_exempt
def delete_bid(request, id):
    listing = Listing.objects.get(id=id)
    bid = Bid.objects.get(id=listing.currentBid.id)
    listing.currentBid = None
    listing.save()
    bid.delete()
    return render(request, "auctions/item.html", {
        "listing": listing
    })
