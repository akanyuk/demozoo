# Generated by Django 3.1.7 on 2021-03-21 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0019_soundtrack_limit_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='hide_from_search_engines',
            field=models.BooleanField(default=False),
        ),
    ]
