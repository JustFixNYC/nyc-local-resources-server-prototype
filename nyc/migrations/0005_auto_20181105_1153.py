# Generated by Django 2.1.2 on 2018-11-05 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nyc', '0004_auto_20181105_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitydistrict',
            name='name',
            field=models.CharField(max_length=80),
        ),
    ]
