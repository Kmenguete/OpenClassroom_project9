# Generated by Django 4.0.5 on 2022-06-27 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0007_alter_review_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="ticket",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="reviews.ticket",
            ),
        ),
    ]
