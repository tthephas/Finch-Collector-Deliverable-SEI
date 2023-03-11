# Generated by Django 4.1.7 on 2023-03-11 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0003_toy_alter_feeding_options_alter_feeding_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.CharField(max_length=200)),
                (
                    "finch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main_app.finch"
                    ),
                ),
            ],
        ),
    ]
