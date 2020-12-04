# Generated by Django 3.1.1 on 2020-12-02 23:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0018_auto_20201201_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArbInstRu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arb_inst', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='userrequest',
            name='type',
        ),
        migrations.CreateModel(
            name='UserRequestRu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('arbs', models.IntegerField(choices=[(1, '1'), (3, '3')], default=3)),
                ('proc', models.CharField(choices=[('Standard', 'Стандартная'), ('Expedited', 'Ускоренная')], default='Standard', max_length=16)),
                ('type', models.CharField(choices=[('Domestic', 'Внутренний'), ('Corporate', 'Корпоративный')], default='Domestic', max_length=16)),
                ('ai', models.ManyToManyField(to='calc.ArbInstRu')),
            ],
        ),
    ]