import pandas as pd
import tweepy
import mongoengine
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from api.models import Task, Tweet, Users
from api.serializers import TaskSerializer, TweetSerializer, UserSerializer
from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler
from rest_framework import views,serializers
from datetime import datetime
from djangorest.settings import auth

class TaskViewSet(views.APIView):
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        l = StdOutListener(serializer.data['count'], serializer.data['search'])
        stream = Stream(auth, l)
        stream.filter(track=serializer.data['search'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def saveData(data, keyword):
    try:
        x = Users.objects.get(use_id=data['user']['id'])

    except Users.DoesNotExist:
        x = Users.objects.create(
                use_id = data['user']['id'],
                name = data['user']['name'],
                friend_count = data['user']['friends_count'],
                screen_name = data['user']['screen_name'],
                location = data['user']['location'],
        )
    tool = Tweet.objects.create(
            user = x,
            tweetedOn = datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
            hashtags  = [x['text'] for x in data['entities']['hashtags']],
            lang = data['lang'],
            retweet_count = data['retweet_count'],
            text = data['text']
        )

def filter_resp(data,queryset_list,user_queryset_list):
    result={}
    if data:
            if(data.get('filters')!=None):
                for x in data['filters']:
                    if(x['operand']=='language'):
                        queryset_list = queryset_list.filter(lang = x['value'])

                    if(x['operand']=='retweet_count'):
                        if(x['operator']=='gte'):
                            queryset_list = queryset_list.filter(retweet_count__gte = x['value'])
                        elif(x['operator']=='gt'):
                            queryset_list = queryset_list.filter(retweet_count__gt = x['value'])
                        elif(x['operator']=='lte'):
                            queryset_list = queryset_list.filter(retweet_count__lte = x['value'])
                        elif(x['operator']=='lt'):
                            queryset_list = queryset_list.filter(retweet_count__lt = x['value'])
                        elif(x['operator']=='eq'):
                            queryset_list = queryset_list.filter(retweet_count = x['value'])

                    elif(x['operand']=='tweetedOn'):
                        # date = (datetime.strptime(x['value'], '%a, %d %b %Y %H:%M:%S'))
                        date, month, year = map(int, x['value'].strip().split("-"))
                        f_date = datetime(year,month, date)
                        if(x['operator']=='gte'):
                            queryset_list = queryset_list.filter(tweetedOn__gte = f_date)
                        elif(x['operator']=='gt'):
                            queryset_list = queryset_list.filter(tweetedOn__gt = f_date)
                        elif(x['operator']=='lte'):
                            queryset_list = queryset_list.filter(tweetedOn__lte = f_date)
                        elif(x['operator']=='lt'):
                            queryset_list = queryset_list.filter(tweetedOn__lt = f_date)
                        elif(x['operator']=='eq'):
                            queryset_list = queryset_list.filter(tweetedOn = f_date)

            if(data.get('searchTerm')!=None):
                queryset_list = queryset_list.filter(text__icontains = data['searchTerm'])


            if(data.get('sort')!=None):
                for x in data['sort']:
                    if(x.get('retweet_count')!=None):
                        if(x['retweet_count']=="desc"):
                            queryset_list = queryset_list.order_by('-retweet_count')
                        if(x['retweet_count']=="asc"):
                            queryset_list = queryset_list.order_by('retweet_count')

                    if(x.get('text')!=None):
                        if(x['text']=="asc"):
                            queryset_list = queryset_list.order_by('text')
                        if(x['text']=="desc"):
                            queryset_list = queryset_list.order_by('-text')


            i=1
            for x in queryset_list:
                result[i]={}
                result[i]['language']=x.lang
                result[i]['name']=x.user.name
                result[i]['hashtags']=x.hashtags
                result[i]['tweetedOn']=x.tweetedOn
                result[i]['text']=x.text
                i=i+1
    return (result)


class StdOutListener(StreamListener):

    def __init__(self, count, keyword):
        self.max_count = int(count)
        self.tweetcount = 0
        self.keyword = keyword

    def on_data(self, data):
        data = json.loads(data)
        saveData(data, self.keyword)
        self.tweetcount+=1

        if self.max_count and self.tweetcount >= self.max_count:
            return (False)

        return (True)

    def on_error(self, status):
        print (status)


class TaskFilterSet(views.APIView):
    # pagination_class=LimitOffsetPagination

    def post(self, request):
        paginate_by=10
        queryset_list = Tweet.objects.all()
        user_queryset_list = Users.objects.all()
        data = request.data
        result={}
        result = filter_resp(data,queryset_list,user_queryset_list)

        if result:
            paginator = PageNumberPagination()
            paginator.page_size = 4
            result_page = paginator.paginate_queryset(queryset_list, request)
            return paginator.get_paginated_response(result)

        else:
            return Response(
                "No results according to your query", status=status.HTTP_400_BAD_REQUEST)



class GetCSV(views.APIView):
    def post(self, request):
        queryset_list = Tweet.objects.all()
        user_queryset_list = Users.objects.all()
        data = request.data
        result = filter_resp(data,queryset_list,user_queryset_list)
        if result:
            df = pd.DataFrame.from_dict(result,orient="index")
            df.to_csv('results.csv')
            return Response("CSV file created", status=status.HTTP_201_CREATED)
        else:
            return Response("No results found.")
