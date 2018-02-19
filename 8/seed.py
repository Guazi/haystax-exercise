import random
from pymongo import MongoClient
# words.py contains approx. 1500 nouns
from words import nouns
from datetime import datetime, date, timedelta

# see class MongoClient from pymongo for connection strings, change as applicable to your situation
db = MongoClient(connect=False)
# we are using the haystax database with a collection name of haystax
collection = db.haystax.haystax

def random_date(start, end):
    return start + timedelta(
        # Get a random amount of seconds between start and end
        seconds=random.randint(0, int((end - start).total_seconds())), )

# we seed with a random date between p1 and p2
# p1 is today - 3 days
p1 = datetime.today() - timedelta(days=3)
# p2 is today + 1 day
p2 = datetime.today() + timedelta(days=1)

dates = []

# seed range(n) random dates/times
for _ in range(1000):
    dates.append(random_date(p1, p2))


seeddata = {}

history = []

for x in dates:
    seed = {}
    seed['date'] = x
    seed['words'] = []
    # seed 10 words for each date
    for _ in range(10):
        # random choice from up to 50 words
        seed['words'].append(random.choice(nouns[:50]))
    history.append(seed)

seeddata['history'] = history

# update the collection for each document
for x in history:
    collection.update(
        {
            "date": x.get('date'),
        }, {"$set": dict(x)}, upsert=True)
