from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
import datetime

# class Poll(Document):
#     question = StringField(max_length=200)
#     pub_date = DateTimeField(help_text='date published')
#     choices = ListField(EmbeddedDocumentField(Choice))


from mongoengine import Document, EmbeddedDocument, fields


class Task(Document):
    search = fields.StringField()
    count = fields.IntField()

class Users(Document):
	use_id = fields.IntField()
	name = fields.StringField()
	friend_count = fields.IntField()
	screen_name = fields.StringField()
	location = fields.StringField()

class Tweet(Document):
	user = fields.ReferenceField(Users, dbref=True)
	tweetedOn = fields.DateTimeField(default=datetime.datetime.now)
	hashtags = fields.ListField()
	lang = fields.StringField()
	retweet_count = fields.IntField()
	text = fields.StringField()

	# meta = {'allow_inheritance': True}
