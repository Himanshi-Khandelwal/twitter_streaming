# Generated by Django 2.0.2 on 2018-02-11 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_taskfilter_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskfilter',
            old_name='text',
            new_name='word',
        ),
    ]
