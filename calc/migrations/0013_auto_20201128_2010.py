# Generated by Django 3.1.1 on 2020-11-28 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0012_auto_20201126_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequest',
            name='ea',
            field=models.IntegerField(choices=[('Yes', 'Yes'), ('No', 'No')], default=2),
        ),
        migrations.AlterField(
            model_name='userrequest',
            name='parties',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], default='No'),
        ),
    ]
