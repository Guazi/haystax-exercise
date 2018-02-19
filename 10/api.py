import twitter
import json
import pytz
import nltk
from bson import json_util
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from email.utils import parsedate_tz, mktime_tz
from nltk.corpus import words, wordnet

# download the wordnet english dictionary
nltk.download('wordnet')

# Twitter API keys (read only)
consumerkey = '7xz7Bzs2UpUNXkY0L1RW37SIE'
consumersecret = '7MTCkwG9j0clVpiaspw31c1tXUvHgfZf4mBFIc0LuhrS2jMJO4'
accesstokenkey = '2586712694-iB9EeQCUTKYXxMlENLlv1E9YXSmgj0owj3vnzRk'
accesstokensecret = 'mwKb6mEh9jOaZylOkmS2k26DKELGqxjsGXVcCLBrfyeFv'

# init the connection to the twitter api
api = twitter.Api(
    consumer_key=consumerkey,
    consumer_secret=consumersecret,
    access_token_key=accesstokenkey,
    access_token_secret=accesstokensecret,
    tweet_mode="extended")

# Initialize Flask
app = Flask(__name__)
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

def to_local_time(tweet_time_string):
    """Convert rfc 5322 -like time string into a local time
       string in rfc 3339 -like format.

    """
    timestamp = mktime_tz(parsedate_tz(tweet_time_string))
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/twitter', methods=['GET'])
def get_five_tweet():
    if request.method == 'GET':
        # Get the twitter handle param from the API request
        handle = request.args.get('handle')
        # init output list
        output = []
        # If the GET request has a handle param, return a response
        if handle:
            # catch invalid requests
            try:
                # send the api request to the Twitter API, max 5 responses
                t = api.GetUserTimeline(screen_name=handle, count=5)
                # transform the response into a dict w/ list comprehension
                tweets = [i.AsDict() for i in t]
                # iterate over each of the 5 tweets
                for t in tweets:
                    print(t)
                    # init an empty dict to form the response, append to output later
                    tweetDict = {}
                    # full text (non-truncated) response
                    tweetDict['full_text'] = t.get('full_text')
                    # Get the time created from the tweet and transform to EST
                    created = t.get('created_at')
                    tweetDict['date'] = to_local_time(created)
                    # total num of words in the tweet
                    tweetDict['totalwords'] = len(t.get('full_text').split())
                    # init english words int at zero
                    tweetDict['english'] = 0
                    # iterate each word to see if in english dictionary
                    for x in t.get('full_text').split():
                        # use the NLTK framework to see if the word is in the english dictonary
                        if wordnet.synsets(x):
                            # if it is, increment english
                            tweetDict['english'] += 1
                    # calculate percentage of tweets that are in English to display on front end
                    tweetDict['percentenglish'] = int(tweetDict['english']/tweetDict['totalwords']*100)
                    # append the dict to output
                    output.append(json.loads(json_util.dumps(tweetDict)))
                    # return the response to the client, jsonify it first
                return jsonify(output)
                # if the handle is invalid or doesn't exist, return an error
            except twitter.error.TwitterError:
                return ("Not a valid handle")
                # if the user didn't include a handle, return an empty response
        elif not handle:
            print("handle not included")
            return jsonify(output)

# run the app using the following command 'python api.py'
if __name__ == '__main__':
    app.run(debug=True, port=4002, threaded=True, host='0.0.0.0')
