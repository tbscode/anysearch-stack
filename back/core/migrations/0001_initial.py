# Generated by Django 4.1.2 on 2023-04-29 13:54

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('show_second_name', models.BooleanField(default=False)),
                ('hash', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_boss', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('second_name', models.CharField(max_length=50)),
                ('language', models.CharField(choices=[('english', 'English'), ('german', 'German'), ('spanish', 'Spanish'), ('french', 'French'), ('italian', 'Italian'), ('dutch', 'Dutch'), ('portuguese', 'Portuguese'), ('russian', 'Russian'), ('chinese', 'Chinese'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('arabic', 'Arabic'), ('turkish', 'Turkish'), ('swedish', 'Swedish'), ('polish', 'Polish'), ('danish', 'Danish'), ('norwegian', 'Norwegian'), ('finnish', 'Finnish'), ('greek', 'Greek'), ('czech', 'Czech'), ('hungarian', 'Hungarian'), ('romanian', 'Romanian'), ('indonesian', 'Indonesian'), ('hebrew', 'Hebrew'), ('thai', 'Thai'), ('vietnamese', 'Vietnamese'), ('ukrainian', 'Ukrainian'), ('slovak', 'Slovak'), ('croatian', 'Croatian'), ('serbian', 'Serbian'), ('bulgarian', 'Bulgarian'), ('lithuanian', 'Lithuanian'), ('latvian', 'Latvian'), ('estonian', 'Estonian'), ('persian', 'Persian'), ('afrikaans', 'Afrikaans'), ('swahili', 'Swahili')], default='english', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_second_name', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('base_language', models.CharField(choices=[('english', 'English'), ('german', 'German'), ('spanish', 'Spanish'), ('french', 'French'), ('italian', 'Italian'), ('dutch', 'Dutch'), ('portuguese', 'Portuguese'), ('russian', 'Russian'), ('chinese', 'Chinese'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('arabic', 'Arabic'), ('turkish', 'Turkish'), ('swedish', 'Swedish'), ('polish', 'Polish'), ('danish', 'Danish'), ('norwegian', 'Norwegian'), ('finnish', 'Finnish'), ('greek', 'Greek'), ('czech', 'Czech'), ('hungarian', 'Hungarian'), ('romanian', 'Romanian'), ('indonesian', 'Indonesian'), ('hebrew', 'Hebrew'), ('thai', 'Thai'), ('vietnamese', 'Vietnamese'), ('ukrainian', 'Ukrainian'), ('slovak', 'Slovak'), ('croatian', 'Croatian'), ('serbian', 'Serbian'), ('bulgarian', 'Bulgarian'), ('lithuanian', 'Lithuanian'), ('latvian', 'Latvian'), ('estonian', 'Estonian'), ('persian', 'Persian'), ('afrikaans', 'Afrikaans'), ('swahili', 'Swahili')], default='english', max_length=255)),
                ('participants', models.ManyToManyField(blank=True, null=True, related_name='project_participants', to=settings.AUTH_USER_MODEL)),
                ('users_connected', models.ManyToManyField(blank=True, null=True, related_name='project_users_connected', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('original_message', models.TextField()),
                ('data', models.JSONField()),
                ('hash', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file_attachment', models.BinaryField(blank=True, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_messages', to='core.project')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile'),
        ),
        migrations.AddField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_projects', to='core.project'),
        ),
        migrations.AddField(
            model_name='user',
            name='settings',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.usersetting'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
