# Generated by Django 3.1.7 on 2021-06-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="telegram_id",
            field=models.PositiveBigIntegerField(null=True, unique=True),
        ),
    ]