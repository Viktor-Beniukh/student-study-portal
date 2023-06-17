# Generated by Django 4.2.2 on 2023-06-17 18:57

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_add_user"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", user.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
    ]