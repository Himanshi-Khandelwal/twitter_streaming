# Generated by Django 2.0.2 on 2018-02-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('text', models.TextField()),
            ],
        ),
    ]