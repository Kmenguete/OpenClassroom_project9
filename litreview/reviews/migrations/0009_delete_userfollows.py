# Generated by Django 4.0.5 on 2022-07-25 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0008_alter_review_ticket"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserFollows",
        ),
    ]