# Generated by Django 5.0.3 on 2024-03-14 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0004_inventoryitem_assigned_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventoryitem",
            name="assigned_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
