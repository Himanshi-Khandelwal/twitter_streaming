# Generated by Django 2.0.2 on 2018-02-11 14:37

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180211_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskfilter',
            name='retweet_count',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
