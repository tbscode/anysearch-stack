# Generated by Django 4.1.2 on 2023-04-30 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='file_meta',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='base_language',
            field=models.CharField(choices=[('english', 'English'), ('german', 'German'), ('spanish', 'Spanish'), ('french', 'French'), ('italian', 'Italian'), ('dutch', 'Dutch'), ('portuguese', 'Portuguese'), ('russian', 'Russian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('arabic', 'Arabic'), ('turkish', 'Turkish'), ('swedish', 'Swedish'), ('polish', 'Polish'), ('danish', 'Danish'), ('norwegian', 'Norwegian'), ('finnish', 'Finnish'), ('greek', 'Greek'), ('hungarian', 'Hungarian'), ('romanian', 'Romanian'), ('indonesian', 'Indonesian'), ('hebrew', 'Hebrew'), ('thai', 'Thai'), ('ukrainian', 'Ukrainian'), ('serbian', 'Serbian'), ('latvian', 'Latvian'), ('estonian', 'Estonian'), ('afrikaans', 'Afrikaans'), ('swahili', 'Swahili')], default='english', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(choices=[('english', 'English'), ('german', 'German'), ('spanish', 'Spanish'), ('french', 'French'), ('italian', 'Italian'), ('dutch', 'Dutch'), ('portuguese', 'Portuguese'), ('russian', 'Russian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('arabic', 'Arabic'), ('turkish', 'Turkish'), ('swedish', 'Swedish'), ('polish', 'Polish'), ('danish', 'Danish'), ('norwegian', 'Norwegian'), ('finnish', 'Finnish'), ('greek', 'Greek'), ('hungarian', 'Hungarian'), ('romanian', 'Romanian'), ('indonesian', 'Indonesian'), ('hebrew', 'Hebrew'), ('thai', 'Thai'), ('ukrainian', 'Ukrainian'), ('serbian', 'Serbian'), ('latvian', 'Latvian'), ('estonian', 'Estonian'), ('afrikaans', 'Afrikaans'), ('swahili', 'Swahili')], default='english', max_length=50),
        ),
    ]
