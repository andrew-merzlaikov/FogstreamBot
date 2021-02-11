# Generated by Django 3.1.6 on 2021-02-11 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appadmin', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='confirm',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_confirm',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_not_confirm',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
