from django import forms
from .models import Listing, Comment, Bid

class CreateListingForm(forms.ModelForm):
    
    class Meta:
        model = Listing
        fields = ("title", "description", "start_bid", "image_url", "category",)
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("comment",)

class BidForm(forms.ModelForm):
    
    class Meta:
        model = Bid
        fields = ("bid",)

