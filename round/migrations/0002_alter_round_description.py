# Generated by Django 3.2.5 on 2021-12-25 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('round', '0001_initial_squashed_0007_big_shake_up_finalized'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
