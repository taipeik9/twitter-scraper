import json
import urllib

import scrapy
from scrapy import signals
from scrapy.exceptions import CloseSpider


class TweetSpider(scrapy.Spider):
    name = "tweets"
    allowed_domains = ["www.twitter.com", "api.twitter.com", "twitter.com"]
    init_bottom_cursor = ""
    direction = "TOP"
    tweet_list = []

    # Twitter API Public Bearer token
    bearer = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

    def __init__(self, query="", limit=None, *args, **kwargs):
        super(TweetSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.limit = limit

    def start_requests(self):
        if not self.query:
            raise CloseSpider("Query argument needed. Check the ReadMe")

        yield scrapy.Request(
            url="http://api.twitter.com/1.1/guest/activate.json",
            method="POST",
            headers={"Authorization": self.bearer},
        )
        self.params = {
            "include_profile_interstitial_type": "1",
            "include_blocking": "1",
            "include_blocked_by": "1",
            "include_followed_by": "1",
            "include_want_retweets": "1",
            "include_mute_edge": "1",
            "include_can_dm": "1",
            "include_can_media_tag": "1",
            "skip_status": "1",
            "cards_platform": "Web-12",
            "include_cards": "1",
            "include_ext_alt_text": "true",
            "include_quote_count": "true",
            "include_reply_count": "1",
            "tweet_mode": "extended",
            "include_entities": "true",
            "include_user_entities": "true",
            "include_ext_media_color": "true",
            "include_ext_media_availability": "true",
            "send_error_codes": "true",
            "simple_quoted_tweets": "true",
            # "q": f"{self.query}-filter:replies",
            "q": f"{self.query} include:nativeretweets",
            "tweet_search_mode": "live",
            "count": "100",
            "query_source": "typed_query",
            "cursor": None,
            "pc": "1",
            "spelling_corrections": "1",
            "ext": "mediaStats,highlightedLabel",
        }

    def parse(self, response):
        r = json.loads(response.body)
        self.guest_token = r["guest_token"]

        yield scrapy.Request(
            url="https://twitter.com/i/api/2/search/adaptive.json?"
            + urllib.parse.urlencode(self.params),
            headers={"x-guest-token": self.guest_token, "authorization": self.bearer},
            meta={"cursor": None},
            callback=self.parse_search,
        )

    def parse_search(self, response):
        search_json = json.loads(response.body)
        tweets = search_json["globalObjects"]["tweets"]
        users = search_json["globalObjects"]["users"]
        instructions = search_json["timeline"]["instructions"]

        if not tweets and self.direction == 'BOTTOM':
            raise CloseSpider("Finished")

        for obj in tweets:
            tweet_dict = {
                "id" : tweets[obj]['id'],
                "tweet": tweets[obj]["full_text"],
                "created": tweets[obj]["created_at"],
                "name": users[tweets[obj]["user_id_str"]]["name"],
                "screen_name": users[tweets[obj]["user_id_str"]]["screen_name"],
                "location": users[tweets[obj]["user_id_str"]]["location"],
            }
            yield tweet_dict
            self.tweet_list.append(tweet_dict)

        if self.limit:
            if len(self.tweet_list) >= self.limit:
                raise CloseSpider("Limit reached")

        for instruction in instructions:
            if "addEntries" in instruction:
                entries = instruction["addEntries"]["entries"]
            elif "replaceEntry" in instruction:
                entries = [instruction["replaceEntry"]["entry"]]
            else:
                continue

            for entry in entries:
                if not entry["entryId"].startswith("sq-cursor-"):
                    continue
                if entry["entryId"] == "sq-cursor-top":
                    top_cursor = entry["content"]["operation"]["cursor"]["value"]
                if entry["entryId"] == "sq-cursor-bottom":
                    bottom_cursor = entry["content"]["operation"]["cursor"]["value"]
                    if not self.init_bottom_cursor:
                        self.init_bottom_cursor = entry["content"]["operation"][
                            "cursor"
                        ]["value"]

        if not tweets and self.direction == "TOP":
            cursor = self.init_bottom_cursor
            self.direction = "BOTTOM"
        elif tweets and self.direction == "TOP":
            cursor = top_cursor
        else:
            cursor = bottom_cursor

        req_params = self.params.copy()
        req_params["cursor"] = cursor

        yield scrapy.Request(
            url="https://twitter.com/i/api/2/search/adaptive.json?"
            + urllib.parse.urlencode(req_params),
            headers={"x-guest-token": self.guest_token, "authorization": self.bearer},
            callback=self.parse_search,
        )


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TweetSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        """
        Everything here happens after data has been scraped and spider has been closed
        """

        # Additional processing can happen here
        pass
