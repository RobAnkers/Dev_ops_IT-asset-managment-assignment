# Generated by Django 5.0.3 on 2024-03-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0005_alter_inventoryitem_assigned_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventoryitem",
            name="last_edited",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
