# Generated by Django 4.2.1 on 2023-05-25 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webtool", "0002_alter_tool_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tool",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]