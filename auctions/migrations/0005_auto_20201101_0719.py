# Generated by Django 2.2.15 on 2020-11-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201031_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
