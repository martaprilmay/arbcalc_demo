# Generated by Django 3.1.1 on 2020-11-26 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0011_userrequest_ea'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='parties',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], default=2),
        ),
        migrations.AlterField(
            model_name='userrequest',
            name='ea',
            field=models.IntegerField(choices=[(1, 'Emergency Arbitrator'), (2, 'No')], default=2),
        ),
    ]
