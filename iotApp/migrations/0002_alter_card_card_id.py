# Generated by Django 4.2.6 on 2023-11-02 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_id',
            field=models.CharField(default='null', max_length=100, primary_key=True, serialize=False),
        ),
    ]
