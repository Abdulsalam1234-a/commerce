# Generated by Django 4.1.7 on 2023-10-26 13:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist_user_remove_watchlist_list_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist_listing', to=settings.AUTH_USER_MODEL),
        ),
    ]
