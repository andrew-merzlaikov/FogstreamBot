# Generated by Django 3.1.6 on 2021-02-12 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appadmin', '0004_auto_20210211_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='confirm',
        ),
        migrations.DeleteModel(
            name='Message_Info',
        ),
    ]