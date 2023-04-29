from django.db import models
from googletrans import Translator
from googletrans.constants import LANGUAGES
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import AbstractUser, BaseUserManager
import concurrent.futures
import base64
from uuid import uuid4
import random


class LanguageChoices(models.TextChoices):
    ENGLISH = "english", pgettext_lazy("profile.lang.english", "English")
    GERMAN = "german", pgettext_lazy("profile.lang.german", "German")
    SPANISH = "spanish", pgettext_lazy("profile.lang.spanish", "Spanish")
    FRENCH = "french", pgettext_lazy("profile.lang.french", "French")
    ITALIAN = "italian", pgettext_lazy("profile.lang.italian", "Italian")
    DUTCH = "dutch", pgettext_lazy("profile.lang.dutch", "Dutch")
    PORTUGUESE = "portuguese", pgettext_lazy(
        "profile.lang.portuguese", "Portuguese")
    RUSSIAN = "russian", pgettext_lazy("profile.lang.russian", "Russian")
    JAPANESE = "japanese", pgettext_lazy(
        "profile.lang.japanese", "Japanese")
    KOREAN = "korean", pgettext_lazy("profile.lang.korean", "Korean")
    ARABIC = "arabic", pgettext_lazy("profile.lang.arabic", "Arabic")
    TURKISH = "turkish", pgettext_lazy("profile.lang.turkish", "Turkish")
    SWEDISH = "swedish", pgettext_lazy("profile.lang.swedish", "Swedish")
    POLISH = "polish", pgettext_lazy("profile.lang.polish", "Polish")
    DANISH = "danish", pgettext_lazy("profile.lang.danish", "Danish")
    NORWEGIAN = "norwegian", pgettext_lazy(
        "profile.lang.norwegian", "Norwegian")
    FINNISH = "finnish", pgettext_lazy("profile.lang.finnish", "Finnish")
    GREEK = "greek", pgettext_lazy("profile.lang.greek", "Greek")
    HUNGARIAN = "hungarian", pgettext_lazy(
        "profile.lang.hungarian", "Hungarian")
    ROMANIAN = "romanian", pgettext_lazy(
        "profile.lang.romanian", "Romanian")
    INDONESIAN = "indonesian", pgettext_lazy(
        "profile.lang.indonesian", "Indonesian")
    HEBREW = "hebrew", pgettext_lazy("profile.lang.hebrew", "Hebrew")
    THAI = "thai", pgettext_lazy("profile.lang.thai", "Thai")
    UKRAINIAN = "ukrainian", pgettext_lazy(
        "profile.lang.ukrainian", "Ukrainian")
    SERBIAN = "serbian", pgettext_lazy("profile.lang.serbian", "Serbian")
    LATVIAN = "latvian", pgettext_lazy("profile.lang.latvian", "Latvian")
    ESTONIAN = "estonian", pgettext_lazy(
        "profile.lang.estonian", "Estonian")
    AFRIKAANS = "afrikaans", pgettext_lazy(
        "profile.lang.afrikaans", "Afrikaans")
    SWAHILI = "swahili", pgettext_lazy("profile.lang.swahili", "Swahili")


def get_random_language():
    choices = [lang[0] for lang in LanguageChoices.choices]
    return random.choice(choices)


class UserManager(BaseUserManager):
    def create(self, password, **kwargs):
        user = self.model(
            profile=UserProfile.objects.create(),
            settings=UserSetting.objects.create(),
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        user = self.create(password, **kwargs)
        return user


class User(AbstractUser):
    objects = UserManager()
    show_second_name = models.BooleanField(default=False)

    hash = models.UUIDField(default=uuid4, editable=False, unique=True)

    profile = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE)
    settings = models.OneToOneField(
        'UserSetting', on_delete=models.CASCADE)

    is_boss = models.BooleanField(default=False)

    projects = models.ManyToManyField(
        'Project', related_name='user_projects', blank=True, null=True)


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    image = models.TextField(null=True, blank=True)
    language = models.CharField(
        max_length=50, choices=LanguageChoices.choices, default=LanguageChoices.ENGLISH)


class UserSetting(models.Model):

    show_second_name = models.BooleanField(default=False)


class Project(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()

    hash = models.UUIDField(default=uuid4, editable=False, unique=True)

    base_language = models.CharField(
        choices=LanguageChoices.choices,
        default=LanguageChoices.ENGLISH,
        max_length=255)

    participants = models.ManyToManyField(
        User, related_name='project_participants', null=True, blank=True)

    users_connected = models.ManyToManyField(
        User, related_name='project_users_connected', null=True, blank=True)

    ai_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='ai_user')


LANG_TO_SLUG = {y: x for x, y in LANGUAGES.items()}


def translate_text(text, source_lang, dest_lang):
    translator = Translator()
    translation = translator.translate(text, src=source_lang, dest=dest_lang)
    return dest_lang, translation.text


def translate_to_all_langs_in_list(text, lang_list, source_lang):
    data = {}
    source_lang_slug = LANG_TO_SLUG[source_lang]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(
            translate_text, text, source_lang_slug, LANG_TO_SLUG[lang]) for lang in lang_list]

        for future in concurrent.futures.as_completed(futures):
            lang, translation = future.result()
            data[LANGUAGES[lang]] = translation
            print("GOT", translation)

    return data


def get_langs_in_project(project):
    return [str(project.base_language)] + [x.profile.language for x in project.participants.all()]


class ChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='project_messages')

    time = models.DateTimeField(auto_now_add=True)
    original_message = models.TextField()
    data = models.JSONField(default=dict)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='message_user')

    hash = models.UUIDField(default=uuid4, editable=False, unique=True)

    file_attachment = models.BinaryField(blank=True, null=True)

    def get_attachment_b64(self):
        """
        TODO: we will not setup full media file handling for this simple project, ultimatily this should also be changed 
        For simplicicy we just use Binary database field for now and endode this as b64 string to be send to the frontend
        In the frontend you can reconstruct the file with something along the lines of:
        var file = dataURLtoFile('data:text/plain;base64,aGVsbG8gd29ybGQ=','hello.txt');
        console.log(file);
        """
        return base64.b64encode(self.file_attachment).decode('utf-8')
