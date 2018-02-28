# Twitter Streaming API
----
## 3 APIs has been created
1. API for twitter streaming
2. API for search stored tweets
3. API to export filter data in CSV file.

----

####MONDODB is used for storing data.

----
## 1. API to trigger Twitter Stream
This API triggers twitter streaming and store the normalized and curated version
of the tweet data.

API - `http://127.0.0.1:8000/tasks/`

Example


          search : Modi
          count :5

----
## 2. API to filter/search stored tweets
API - `http://127.0.0.1:8000/task-filter/`

Example


      {
    "filters": [
        {
            "operand": "tweetedOn",
            "operator": "gte",
            "value": "15-1-2018"
        },
        {
            "operand": "language",
            "operator": "eq",
            "value": "en"
        }
    ],
    "sort" : [
        {
            "retweet_count": "desc"
        },
        {
            "text": "asc"
        }
    ],
    "searchTerm": "Prize"
}


## 3. API to export filtered data in CSV
API - `http://127.0.0.1:8000/task-csv/`

The query has to be asked in the same way as above and then a csv file containing the filtered data will be created.
