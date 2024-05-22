from django.contrib import admin
from .models import User, Category, Comment, Listing, Watchlist,Bid

class ListingDisplay(admin.ModelAdmin):
    list_display = ("id", "title", "category", "owner", "start_bid", "is_active")
    
class WatchlistDisplay(admin.ModelAdmin):
    filter_horizontal = ("list_item",)

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Listing, ListingDisplay)
admin.site.register(Watchlist, WatchlistDisplay)
admin.site.register(Bid)