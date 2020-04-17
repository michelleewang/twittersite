import datetime

from django.db import models
from django.utils import timezone


class Tweet(models.Model): # tweet class
    tweet_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.tweet_text + " " + str(self.id)
    def was_published_recently(self): # check if tweet was created recently
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Comment(models.Model): # comment class
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return self.comment_text
