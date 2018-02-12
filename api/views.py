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
from api.models import Task, TaskFilter
from api.serializers import TaskSerializer, TaskFilterSerializer
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from djangorest.settings import tweet_collection, twitter_api
# from bson import ObjectId
# from bson.json_util import dumps


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


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
