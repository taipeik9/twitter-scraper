
# No Limit Twitter Scraper

Unlimited Twitter scraper using the public API, no API Key needed.

To use the scraper cd into the twitter folder and ```docker-compose up``` with the ```--build``` tag if this is the first time using.

The search is currently set to scrape tweets from Elon Musk with no limit, in order from most recent to least recent. To edit the search, open the docker-compose.yml in the twitter folder and change the command. There are currently two arguments you can use with the scrape:

- query (str): the desired search, this is where you can use all of the search operators.
- limit (optional), default None. The limit of tweets you would like to scrape. If you are doing a general search, it would be helpful to set a limit or the scraper will run for a long time.

Example of command line using both query and limit arguments:
```
scrapy crawl tweets -o 'data/tweets.csv' -a query="from:elonmusk" -a limit=500
```

In the search_params.md there are a list of search parameters that you can change in the spider (./twitter/twitter/spiders/tweets.py)

## Search Operators

Operator -- Finds Tweets

watching now -- containing both “watching” and “now”. This is the default operator.

#haiku -- containing the hashtag “haiku”.

“happy hour” -- containing the exact phrase “happy hour”.

to:NASA	a Tweet authored in reply to Twitter account “NASA”.

@NASA -- mentioning Twitter account “NASA”.

love OR hate -- containing either “love” or “hate” (or both).

beer -root -- containing “beer” but not “root”.

from:interior -- sent from Twitter account “interior”.

list:NASA/astronauts-in-space-now -- sent from a Twitter account in the NASA list astronauts-in-space-now

superhero since:2015-12-21 -- containing “superhero” and sent since date “2015-12-21” (year-month-day).

puppy until:2015-12-21 -- containing “puppy” and sent before the date “2015-12-21”.

**A number of other search operators can be found here in the Twitter API docs:**

https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
