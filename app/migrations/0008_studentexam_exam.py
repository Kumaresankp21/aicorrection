# Generated by Django 5.1.5 on 2025-02-22 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_studentexam_evaluation_report"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentexam",
            name="exam",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submissions",
                to="app.exam",
            ),
        ),
    ]
