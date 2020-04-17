from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Tweet, Comment

#def get(request):
#def post(request):

class HomePageView(generic.ListView): # take user to 'home page'
    template_name = 'home.html'
    context_object_name = 'latest_tweet_list'

    def get_queryset(self):
        """ Return the last five published tweets (not including those set to
        be published in the future). """
        """context = {'latest_tweet_list': Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]}
        return context"""
        return Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    """def get(self, request):
        return render(template_name)
    def post(request):
        return"""


class DetailView(generic.DetailView): # take user to a specific tweet
    model = Tweet
    template_name = 'twit/detail.html'
    def get_queryset(self):
        """Excludes any tweets that aren't published yet."""
        return Tweet.objects.filter(pub_date__lte=timezone.now())

class CommentView(generic.DetailView): # take user to commenting screen
    model = Tweet
    template_name = 'twit/comment.html'

def commenting(request, tweet_id): # allow user to leave a comment
    # change code so that it checks if input box is empty and not if a radio button is selected
    # return HttpResponse("You're commenting on tweet %s." % tweet_id)
    print(request.POST)
    tweet = get_object_or_404(Tweet, pk=int(request.POST["tweet_id"]))
    try:
        selected_tweet = Tweet.objects.get(pk=tweet.id)
        print(selected_tweet)
        all_comments = selected_tweet.comment_set.all()
        print(all_comments)
        comment = Comment(tweet=tweet, comment_text=request.POST["comment"])
        comment.save()
        print(comment.id)
    except (KeyError, Comment.DoesNotExist):
        # Redisplay the comment input form
        return render(request, 'twit/detail.html', {
            'tweet': tweet,
            'error_message': "You didn't enter a comment.",
        })
    else:
        #selected_comment.likes += 1
        #selected_comment.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('twit:detail', args=(tweet.id,)))

    """tweet = get_object_or_404(Tweet, pk=tweet_id)
    try:
        selected_choice = tweet.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Commenting.value.length == 0):
        # Redisplay the question voting form.
        return render(request, 'twit/detail.html', {
            'tweet': tweet,
            'error_message': "You didn't enter a comment.",
        })
    else:
        selected_choice. += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('twit:comments', args=(question.id,)))"""
