# Generated by Django 3.1.1 on 2020-12-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0017_auto_20201130_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cost',
            old_name='em_fee',
            new_name='ea_fee',
        ),
        migrations.AddField(
            model_name='userrequest',
            name='type',
            field=models.CharField(choices=[('Domestic', 'Domestic'), ('Corporate', 'Corporate')], default='Domestic', max_length=16),
        ),
        migrations.AlterField(
            model_name='userrequest',
            name='parties',
            field=models.IntegerField(choices=[(2, '2'), (3, '3'), (4, '4')], default=2),
        ),
    ]
