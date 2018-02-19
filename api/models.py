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
    # created = fields.DateTimeField(default=datetime.datetime.now)

class Users(Document):
	user_id = fields.StringField()
	name = fields.StringField()
	friend_count = fields.IntField()

class Tweet(Document):
	tweet_id = fields.ReferenceField(Users, dbref=True)
	created_at = fields.DateTimeField(default=datetime.datetime.now)
	screen_name = fields.StringField()
	user_name = fields.StringField()
	location = fields.StringField()
	text = fields.StringField()
