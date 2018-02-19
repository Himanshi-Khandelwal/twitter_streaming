import csv
import json
import pandas as pd
import tweepy
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from api.models import Task, Tweet, Users
from api.serializers import TaskSerializer, TweetSerializer, UserSerializer
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import mongoengine
# from django.contrib.auth import authenticate
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from django.shortcuts import get_object_or_404
from mongoengine.queryset.visitor import Q
from django.core.exceptions import ObjectDoesNotExist

consumer_key = 'Cu85P1mfYUULhYr3GXYicIsaF'
consumer_secret = '5Ni0Onrl6kD5Vzbw18pdQOWG9oHN2LU3MY8k4fsbaSzAoDl1x5'
access_token = '730266246113988608-temclGmgYJIChkL6ZK36NtqMng0y28W'
access_token_secret = 'y6DoCvWXwzix4lCPDABfvGiMjCuH8EXHfZn2riNJI3jJy'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# from djangorest.settings import auth
# user = authenticate(username='himanshi', password='himanshi')
# assert isinstance(user, mongoengine.django.auth.User)

# from bson import ObjectId
# from bson.json_util import dumps


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)

class TaskViewSet(MongoModelViewSet):

    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all()

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
       
        if not serializer.is_valid():
            return Response("error")
        # serializer.save()

        print(serializer['count'])
        l = StdOutListener(request.data['count'], request.data['search'])   
        stream = Stream(auth, l)
        stream.filter(track=request.data["search"])
        return Response("yo")

def storeTweet(data):
    tool = Tweet.objects.create(
                tweet_id = data['user']['id'],
                created_at = data['created_at'],
                screen_name = data['user']['screen_name'],
                user_name = data['user']['name'],
                location = data['user']['location'],
                text = data['text']
        )

def storeData(data, keyword):
    print(data['user']['id'])
    print(type(data['user']['id']))
    try:
        x = Users.objects.get(user_id=data['user']['id'])
        
    except Users.DoesNotExist:
        x = Users.objects.create(
                user_id = data['user']['id'],
                name = data['user']['name'],
                friend_count = data['user']['friends_count'],
        )

    storeTweet(data);



    # dtest = tweets.find_one({'id':data['id']})
    # if dtest == None:
    #     user_keys = ['id','screen_name', 'name', 'location', 'followers_count']
    #     qtest = users.find_one({'id':data['user']['id']})
    #     if qtest == None:
    #         saveuser = {key: data['user'][key] for key in user_keys}
    #         saveuser["name_lower"] = data['user']['name'].lower()
    #         saveuser["screen_name_lower"] = saveuser["screen_name"].lower()
    #         if data['user']['location']:
    #             saveuser["location_lower"] = data['user']['location'].lower()
    #         users.insert(saveuser)

      


    #     data['user'] = data['user']['id']

    #     data_keys = ['favorite_count', 'id', 'is_quote_status', 'lang', 'retweet_count','user']
    #     savedata = {key: data[key] for key in data_keys}
    #     if data['truncated'] and 'full_text' in data:
    #         savedata['text'] = data['full_text']
    #     else:
    #         savedata['text'] = data['text']

    #     savedata['created_at'] = dt = datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    #     savedata['text_lower'] = savedata['text'].lower()
    #     savedata['hashtags'] = [x['text'] for x in data['entities']['hashtags']]
    #     savedata['hashtags_lower'] = [x['text'].lower() for x in data['entities']['hashtags']]
    #     savedata['user_mentions'] = [x['screen_name'] for x in data['entities']['user_mentions']]
    #     savedata['user_mentions_lower'] = [x['screen_name'].lower() for x in data['entities']['user_mentions']]
    #     savedata['keyword'] = keyword
    #     savedata['is_retweet'] = False
    #     if 'retweeted_status' in data:
    #         savedata['is_retweet'] = True
    #     tweets.insert(savedata)

class StdOutListener(StreamListener):

    def __init__(self, count, keyword):
        self.maxtweet = int(count)
        self.tweetcount = 0
        self.keyword = keyword

    def on_data(self, data):
        dtemp = json.loads(data)
        storeData(dtemp, self.keyword)
        print(dtemp)
        print(self.tweetcount)
        self.tweetcount+=1
        
        if self.maxtweet and self.tweetcount >= self.maxtweet:
            return (False)

        return (True)

    def on_error(self, status):
        print (status)


@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 4
        tasks = Task.objects.all()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            query = serializer.data
            search_results = twitter_api.search.tweets(count=100, q=query)
            statuses = search_results["statuses"]
            tweets = {}
            resp = []
            for statuse in statuses:
                tweet_collection.remove({"text": statuse['text']})
                try:
                    tweets = {'text': statuse['text'],
                              'id': statuse['id_str'],
                              'created_at': statuse['created_at'],
                              'retweet_count': statuse['retweet_count'],
                              'favorite_count': statuse['favorite_count'],
                              'metadata': statuse['metadata']}
                    if(statuse['entities']['user_mentions'][0]):
                        tweets['screen_name'] = (statuse['entities']['user_mentions'][0]['screen_name'])
                    resp.append(tweets)
                    tweet_collection.insert(tweets)
                except:
                    pass
            if not tweets:
                    return Response("No results",
                                    status=status.HTTP_201_CREATED)
            for i in resp:
                i['_id'] = str(i['_id'])
            return Response((resp), status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def task_filter(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 4
        tasks = Task.objects.all()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        if request.data:
            tweet_cursor = tweet_collection.find().sort(
                                        [("created_at", 1), ("text", 1)])
            resp = []
            tweet_cursor = tweet_collection.find(request.data)
            for statuse in tweet_cursor:
                tweets = {}
                try:
                    tweets = {'created_at':statuse['created_at'], 'retweet_count':statuse['retweet_count'], 'favorite':statuse['favorite_count'],'text':statuse['text']}            #         pprint(statuse['created_at'])
                    resp.append(tweets)
                    df = pd.DataFrame(resp, columns=['created_at', 'retweet_count', 'text'])
                    df.to_csv('example.csv')
                except:
                    pass


            return Response(resp, status = status.HTTP_201_CREATED)
        else:
            return Response(
                "Error", status=status.HTTP_400_BAD_REQUEST)
