from pymongo import MongoClient
from datetime import datetime, date, timedelta

# see class MongoClient from pymongo for connection strings, change as applicable to your situation
db = MongoClient(connect=False)
# we are using the haystax database with a collection name of haystax
collection = db.haystax.haystax

today = datetime.today()


def run_through(pipeline):
    sorted = list(collection.aggregate(pipeline))
    return sorted


while True:
    d1a = input(
        "Choose a function: \n A) Most Frequent Word - Overall \n B) Most Frequent Word - 24 Hours \n C) Trending Word - 24 hours \n [A/B/C]? : "
    )
    # check if d1a is equal to one of the strings, specified in the list
    if d1a in ['A', 'B', 'C']:
        # if it was equal - break from the while loop
        break
#  Case A - Most Frequent Word seen in the dataset
if d1a == "A":
    # create a mongoDB pipeline to group on the sum of word count, sorted high-to-low
    pipeline = [{
        # only project the words since this isn't limited by date
        "$project": {
            "words": "$words"
        }
    }, 
    # unwind the words so we count the occurrences of the individual word
    {
        "$unwind": {
            "path": "$words"
        }
    }, 
    # extend the results for a count field, which is a sum of the occurances of the word
    {
        "$group": {
            "_id": "$words",
            "count": {
                "$sum": 1
            }
        }
    }, 
    # sort by # of occurances, high to low
    {
        "$sort": {
            "count": -1
        }
    }]
    # run the aggregation and return the results as a list
    sorted = run_through(pipeline)
    print(
        "The word that occured most frequently in the entire dataset is: {}. It occured {} times.".
        format(sorted[0].get("_id"), sorted[0].get("count")))
#  Case B  - Most Frequent Word seen in the past 24 hours
elif d1a == "B":
    pipeline = [{
        # we project the date here now because we will need to filter it in the match stage
        "$project": {
            "words": "$words",
            "date": 1,
        }
    }, 
    # match only if the date is within the last 24-hours
    {
        "$match": {
            "date": {
                "$gte": today - timedelta(days=1),
                "$lte": today
            }
        }
    }, {
        "$unwind": {
            "path": "$words"
        }
    }, {
        "$group": {
            "_id": "$words",
            "count": {
                "$sum": 1
            }
        }
    }, {
        "$sort": {
            "count": -1
        }
    }]
    sorted = run_through(pipeline)
    print(
        "The word that occured most frequently in the last 24 hours is: {}. It occured {} times.".
        format(sorted[0].get("_id"), sorted[0].get("count")))
#  Case C  - Most trending word
elif d1a == "C":
    # we will need two pipelines, pipeline_today returns results only between now and 24 hours ago
    pipeline_today = [{
        "$project": {
            "words": "$words",
            "date": 1,
        }
    }, {
        "$match": {
            "date": {
                "$gte": today - timedelta(days=1),
                "$lte": today
            }
        }
    }, {
        "$unwind": {
            "path": "$words"
        }
    }, {
        "$group": {
            "_id": "$words",
            "count": {
                "$sum": 1
            }
        }
    }, {
        "$sort": {
            "count": -1
        }
    }]
    # pipeline_yesterday returns results only occuring in the previous 48 hours to 24 hours from now.
    pipeline_yesterday = [{
        "$project": {
            "words": "$words",
            "date": 1,
        }
    }, {
        "$match": {
            "date": {
                "$gte": today - timedelta(days=2),
                "$lte": today - timedelta(days=1)
            }
        }
    }, {
        "$unwind": {
            "path": "$words"
        }
    }, {
        "$group": {
            "_id": "$words",
            "count": {
                "$sum": 1
            }
        }
    }, {
        "$sort": {
            "count": -1
        }
    }]
    # Turn mongoDB repsonse cursor -> list into a dictionary
    today_dict = {x['_id']: x['count'] for x in run_through(pipeline_today)}
    yesterday_dict = {
        x['_id']: x['count']
        for x in run_through(pipeline_yesterday)
    }
    # create a dict with an initial difference_percent of 0
    topDict = {'difference_pct': 0}
    # iterate k,v for all items in the most recent 24-hour dict
    for k, v in today_dict.items():
        # calculate the difference of occurances from today - yesterday values
        # if the word is new, we return the frequency as one instead of zero to avoid ZeroDivisorError
        difference_pct = (v - yesterday_dict.get(k, 1))/yesterday_dict.get(k, 1)
        # if difference_pct is greater than initial value 0 or previous top difference
        if difference_pct > topDict['difference_pct']:
            topDict['word'] = k
            topDict['p2'] = v
            topDict['p1'] = yesterday_dict.get(k, 1)
            topDict['difference_pct'] = (topDict['p2'] - topDict['p1']) / topDict['p1']
    # if we found a word that has a difference greater than 0, then we found the top word
    if topDict.get('word') is not None:
        print(
            "The top trending word is {}. It had an increase in frequency of {} occurrences for a {}% increase."
            "\n It occured {} times in the most recent 24-hour time period, and {} times in the preceeding 24-hour period".
            format(topDict['word'], topDict['p2'] - topDict['p1'], round(topDict['difference_pct']*100, 4), topDict['p2'], topDict['p1'])
            )
    # if we didn't find a word, then nothing had a difference > 0
    elif topDict.get('word') is None:
        print(
            "No word appears in at a greater frequency from the most recent 24-hour time period compared to the preceeding 24-hour period"
        )