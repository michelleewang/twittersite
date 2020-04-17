import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Tweet

def create_tweet(tweet_text, days):
    """
    Create a tweet with the given `tweet_text` and published the
    given number of `days` offset to now (negative for tweets published
    in the past, positive for tweets that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Tweet.objects.create(tweet_text=tweet_text, pub_date=time)

class TweetModelTests(TestCase):

    def test_was_published_recently_with_future_tweet(self):
        """
        was_published_recently() returns False for tweets whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_tweet = Tweet(pub_date=time)
        self.assertIs(future_tweet.was_published_recently(), False)

    def test_was_published_recently_with_old_tweet(self):
        """
        was_published_recently() returns False for tweets whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_tweet = Tweet(pub_date=time)
        self.assertIs(old_tweet.was_published_recently(), False)

    def test_was_published_recently_with_recent_tweet(self):
        """
        was_published_recently() returns True for tweets whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_tweet = Tweet(pub_date=time)
        self.assertIs(recent_tweet.was_published_recently(), True)

class TweetIndexViewTests(TestCase):
    def test_no_tweets(self):
        """
        If no tweets exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('twit:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tweet are available.")
        self.assertQuerysetEqual(response.context['latest_tweet_list'], [])

    def test_past_tweet(self):
        """
        tweets with a pub_date in the past are displayed on the
        index page.
        """
        create_tweet(tweet_text="Past tweet.", days=-30)
        response = self.client.get(reverse('twit:index'))
        self.assertQuerysetEqual(
            response.context['latest_tweet_list'],
            ['<Tweet: Past tweet.>']
        )

    def test_future_tweet(self):
        """
        tweets with a pub_date in the future aren't displayed on
        the index page.
        """
        create_tweet(tweet_text="Future tweet.", days=30)
        response = self.client.get(reverse('twit:index'))
        self.assertContains(response, "No tweet are available.")
        self.assertQuerysetEqual(response.context['latest_tweet_list'], [])

    def test_future_tweet_and_past_tweet(self):
        """
        Even if both past and future tweets exist, only past tweets
        are displayed.
        """
        create_tweet(tweet_text="Past tweet.", days=-30)
        create_tweet(tweet_text="Future tweet.", days=30)
        response = self.client.get(reverse('twit:index'))
        self.assertQuerysetEqual(
            response.context['latest_tweet_list'],
            ['<Tweet: Past tweet.>']
        )

    def test_two_past_tweets(self):
        """
        The tweets index page may display multiple tweets.
        """
        create_tweet(tweet_text="Past tweet 1.", days=-30)
        create_tweet(tweet_text="Past tweet 2.", days=-5)
        response = self.client.get(reverse('twit:index'))
        self.assertQuerysetEqual(
            response.context['latest_tweet_list'],
            ['<Tweet: Past tweet 2.>', '<Tweet: Past tweet 1.>']
        )

class TweetDetailViewTests(TestCase):
    def test_future_tweet(self):
        """
        The detail view of a tweet with a pub_date in the future
        returns a 404 not found.
        """
        future_tweet = create_tweet(tweet_text='Future tweet.', days=5)
        url = reverse('twit:detail', args=(future_tweet.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_tweet(self):
        """
        The detail view of a tweet with a pub_date in the past
        displays the tweet's text.
        """
        past_tweet = create_tweet(tweet_text='Past Tweet.', days=-5)
        url = reverse('twit:detail', args=(past_tweet.id,))
        response = self.client.get(url)
        self.assertContains(response, past_tweet.tweet_text)
