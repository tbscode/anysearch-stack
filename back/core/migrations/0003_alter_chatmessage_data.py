# Generated by Django 4.1.2 on 2023-04-29 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_project_hash_alter_project_base_language_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]