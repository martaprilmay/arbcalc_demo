# Generated by Django 3.1.1 on 2020-11-30 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0014_auto_20201128_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequest',
            name='ea',
            field=models.CharField(default='No', max_length=8),
        ),
    ]
