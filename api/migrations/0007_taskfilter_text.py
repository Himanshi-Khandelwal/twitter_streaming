# Generated by Django 2.0.2 on 2018-02-11 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180211_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfilter',
            name='text',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
