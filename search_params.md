# Search Parameters

These search parameteres are options that could be used in the params dictionary in the tweet scraper. (Not all have been tested)

## Parameter:
q

### Required:
required

### Description:
A UTF-8, URL-encoded search query of 500 characters maximum, including operators. Queries may additionally be limited by complexity.

## Parameter:
geocode

### Required:
optional

### Description:
Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by " latitude,longitude,radius ", where radius units must be specified as either " mi " (miles) or " km " (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly. A maximum of 1,000 distinct "sub-regions" will be considered when using the radius modifier.

### Example:
37.781157 -122.398720 1mi

## Parameter:
tweet_mode

### Required:
optional

### Description:
Set this to extended to ensure that you do not receive truncated tweets

### Example:
extended

## Parameter:
lang

### Required:
optional

### Description:
Restricts tweets to the given language, given by an ISO 639-1 code. Language detection is best-effort.

### Example:
eu

## Parameter:
locale

### Required:
optional

### Description:
Specify the language of the query you are sending (only ja is currently effective). This is intended for language-specific consumers and the default should work in the majority of cases.

### Example:
ja

## Parameter:
result_type

### Required:
optional

### Description:
Specifies what type of search results you would prefer to receive. The current default is "mixed." Valid values include:

* mixed : Include both popular and real time results in the response. (Not Working)
* recent : return only the most recent results in the response
* popular : return only the most popular results in the response.

### Example:
mixed recent popular

## Parameter:
count

### Required:
optional

### Description:
The number of tweets to return per page, up to a maximum of 100. Defaults to 15. This was formerly the "rpp" parameter in the old Search API.

(The public count maximum seems to be 20)

### Example:
100

## Parameter:
until

### Required:
optional

### Description:
Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD. Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.

### Example:
2015-07-19

## Parameter:
since_id

### Required:
optional

### Description:
Returns results with an ID greater than (that is, more recent than) the specified ID. There are limits to the number of Tweets which can be accessed through the API. If the limit of Tweets has occured since the since_id, the since_id will be forced to the oldest ID available.

### Example:
12345

## Parameter:
max_id

### Required:
optional

### Description:
Returns results with an ID less than (that is, older than) or equal to the specified ID.

### Example:
54321

## Parameter:
include_entities

### Required:
optional

### Description:
The entities node will not be included when set to false

### Example:
false

