# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=22)
    name = models.CharField(max_length=255)
    yelping_since = models.DateTimeField()
    review_count = models.IntegerField()
    useful = models.IntegerField()
    funny = models.IntegerField()
    cool = models.IntegerField()
    fans = models.IntegerField()
    average_stars = models.FloatField()
    compliment_hot = models.IntegerField()
    compliment_more = models.IntegerField()
    compliment_profile = models.IntegerField()
    compliment_cute = models.IntegerField()
    compliment_list = models.IntegerField()
    compliment_note = models.IntegerField()
    compliment_plain = models.IntegerField()
    compliment_cool = models.IntegerField()
    compliment_funny = models.IntegerField()
    compliment_writer = models.IntegerField()
    compliment_photos = models.IntegerField()


class Friend(models.Model):
    user = models.ForeignKey(User, related_name='fr_user')
    friend = models.ForeignKey(User, null=True, related_name='fr_friend')


class Business(models.Model):
    business_id = models.CharField(max_length=22)
    name = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    stars = models.FloatField()
    review_count = models.IntegerField()
    is_open = models.IntegerField()


class ReviewText(models.Model):
    text = models.TextField()


class Review(models.Model):
    review_id = models.CharField(max_length=22)
    business = models.ForeignKey(Business)
    user = models.ForeignKey(User)
    text = models.ForeignKey(ReviewText)
    stars = models.IntegerField()
    sentiment = models.FloatField()
    date = models.DateTimeField()
    useful = models.IntegerField()
    funny = models.IntegerField()
    cool = models.IntegerField()

    @property
    def review_text(self):
        return self.text.text


class Photo(models.Model):
    photo_id = models.CharField(max_length=22)
    business = models.ForeignKey(Business)
    caption = models.CharField(max_length=255, default=None)
    label = models.CharField(max_length=255, default=None)
