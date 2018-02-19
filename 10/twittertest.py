

# USING TWEEPY TO GET FULL TEXT

import tweepy
consumerkey = '7xz7Bzs2UpUNXkY0L1RW37SIE'
consumersecret = '7MTCkwG9j0clVpiaspw31c1tXUvHgfZf4mBFIc0LuhrS2jMJO4'
accesstokenkey = '2586712694-iB9EeQCUTKYXxMlENLlv1E9YXSmgj0owj3vnzRk'
accesstokensecret = 'mwKb6mEh9jOaZylOkmS2k26DKELGqxjsGXVcCLBrfyeFv'

auth = tweepy.OAuthHandler(consumerkey, consumersecret)
auth.set_access_token(accesstokenkey, accesstokensecret)

api = tweepy.API(auth)

test = tweepy.Cursor(api.user_timeline,id='FBI', tweet_mode='extended', include_rts = False).items(5)
print(test)

for tweet_info in test:
    print(tweet_info.full_text)

# Using python-twitter for truncated

import twitter

consumerkey = '7xz7Bzs2UpUNXkY0L1RW37SIE'
consumersecret = '7MTCkwG9j0clVpiaspw31c1tXUvHgfZf4mBFIc0LuhrS2jMJO4'
accesstokenkey = '2586712694-iB9EeQCUTKYXxMlENLlv1E9YXSmgj0owj3vnzRk'
accesstokensecret = 'mwKb6mEh9jOaZylOkmS2k26DKELGqxjsGXVcCLBrfyeFv'
api = twitter.Api(
    consumer_key=consumerkey,
    consumer_secret=consumersecret,
    access_token_key=accesstokenkey,
    access_token_secret=accesstokensecret)

t = api.GetUserTimeline(screen_name="akras14", count=10)

tweets = [i.AsDict() for i in t]

for t in tweet:
    print(t)

