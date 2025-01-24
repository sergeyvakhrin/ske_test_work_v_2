# Generated by Django 5.1.5 on 2025-01-24 09:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_alter_warehouse_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="warehouse",
            name="user",
            field=models.ForeignKey(
                default="users.User",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_warehouse",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Организация",
            ),
        ),
    ]
