# Generated by Django 4.0.3 on 2022-03-03 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_add_similarity_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='similarity',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]
