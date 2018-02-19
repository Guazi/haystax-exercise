Exercise:

You have a MongoDB collection with documents which each have a date and an array of words.

1. Find the word that occurs the most frequently in the entire data set.

2. Next, find the word that occurs most frequently in the last 24 hours.

3. Then, find the word that is trending the most - that is, the appearance of this word has increased more than any other word in the last 24 hours over the previous 24 hour period.

Instructions for running the sample:

1. pip install -r requirements.txt

2. Seed the database by running python seed.py from the command line. You may need to edit lines 8 and 10 with your specific connection URI, username/password depending on how you have MongoDB setup. By default, we don't have authentication setup.

3. Run python solution.py. You may need to edit lines 8 and 10 with your specific connection URI. 

4. Select a function by typing A or B or C
