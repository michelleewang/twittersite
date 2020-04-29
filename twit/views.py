from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from googletrans import Translator
from googletrans import LANGUAGES

from .models import Tweet, Comment

#def get(request):
#def post(request):

class HomePageView(generic.ListView): # take user to 'home page'
    #template_name = 'home.html'
    context_object_name = 'latest_tweet_list'

    """def get_queryset(self):
        Return the last five published tweets (not including those set to
        be published in the future).
        context = {'latest_tweet_list': Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]}
        return context
        return Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]"""
    def get(self, request):
        # built-in authenticaion form
        form = AuthenticationForm()
        context = {
            'form': form,
            'allPosts': self.context_object_name,
            'user': request.user,
        }
        return render(request, 'twit/home.html', context)

    def post(self, request):
        if 'logout' in request.POST.keys():
            # log out
            logout(request)
            form = AuthenticationForm()
        else:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # authenticate and log in
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user = user)
        context = {
            'form': form,
            'allPosts': self.context_object_name,
        }
        return render(request, 'twit/home.html', context)


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
        all_comments = selected_tweet.comment_set.all()
        print(request.POST["comment"])
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('twit:detail', args=(tweet.id,)))

def translating(request, tweet_id): # allow user to leave a comment
    # change code so that it checks if input box is empty and not if a radio button is selected
    # return HttpResponse("You're commenting on tweet %s." % tweet_id)
    print(request.POST)
    tweet = get_object_or_404(Tweet, pk=int(request.POST["tweet_id"]))
    try:
        lang = request.POST["lang"]
        print(lang)
        trans = Translator()
        t = trans.translate(
            tweet.tweet_text, src=lang
        )
        print(f'Destination: {t.dest}')
    except (KeyError, lang.DoesNotExist):
        # Redisplay the comment input form
        return render(request, 'twit/detail.html', {
            'tweet': tweet,
            'error_message': "You didn't select a language.",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return return render(request, 'twit/detail.html', {})
        #HttpResponseRedirect(reverse('twit:detail', args=(tweet.id,)))

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
