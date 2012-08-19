from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from busitizer.twitter.tasks import handle_tweet

# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""

class StdOutListener(StreamListener):
	""" A listener handles tweets are the received from the stream. 
	This is a basic listener that just prints received tweets to stdout.

	"""
	def on_data(self, data):
		handle_tweet.delay(data)
		return True

	def on_error(self, status):
		print status


class Command(BaseCommand):
    args = ''
    help = 'Listens for mentions on twitter'

    def handle(self, *args, **options):
    	l = StdOutListener()
    	auth = OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    	auth.set_access_token(settings.TWITTER_OAUTH_KEY, settings.TWITTER_OAUTH_SECRET)

    	stream = Stream(auth, l)	
    	stream.filter(track=['@busitizer'])