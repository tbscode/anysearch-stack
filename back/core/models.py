from django.db import models
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class UserManager(models.Manager):
    def create(self, **kwargs):
        user = self.model(
            profile=UserProfile.objects.create(),
            settings=UserSetting.objects.create(),
            **kwargs,
        )
        user.save(using=self._db)

    def create_superuser(self, number, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        user = self.create(number=number, password=password, **kwargs)
        return user


class User(AbstractUser):
    show_second_name = models.BooleanField(default=False)

    profile = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE)
    settings = models.OneToOneField(
        'UserSetting', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100, blank=True, null=True)

    projects = models.ManyToManyField(
        'Project', related_name='user_projects', blank=True, null=True)


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)


class UserSetting(models.Model):

    show_second_name = models.BooleanField(default=False)


class Project(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()

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
        CHINESE = "chinese", pgettext_lazy("profile.lang.chinese", "Chinese")
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
        CZECH = "czech", pgettext_lazy("profile.lang.czech", "Czech")
        HUNGARIAN = "hungarian", pgettext_lazy(
            "profile.lang.hungarian", "Hungarian")
        ROMANIAN = "romanian", pgettext_lazy(
            "profile.lang.romanian", "Romanian")
        INDONESIAN = "indonesian", pgettext_lazy(
            "profile.lang.indonesian", "Indonesian")
        HEBREW = "hebrew", pgettext_lazy("profile.lang.hebrew", "Hebrew")
        THAI = "thai", pgettext_lazy("profile.lang.thai", "Thai")
        VIETNAMESE = "vietnamese", pgettext_lazy(
            "profile.lang.vietnamese", "Vietnamese")
        UKRAINIAN = "ukrainian", pgettext_lazy(
            "profile.lang.ukrainian", "Ukrainian")
        SLOVAK = "slovak", pgettext_lazy("profile.lang.slovak", "Slovak")
        CROATIAN = "croatian", pgettext_lazy(
            "profile.lang.croatian", "Croatian")
        SERBIAN = "serbian", pgettext_lazy("profile.lang.serbian", "Serbian")
        BULGARIAN = "bulgarian", pgettext_lazy(
            "profile.lang.bulgarian", "Bulgarian")
        LITHUANIAN = "lithuanian", pgettext_lazy(
            "profile.lang.lithuanian", "Lithuanian")
        LATVIAN = "latvian", pgettext_lazy("profile.lang.latvian", "Latvian")
        ESTONIAN = "estonian", pgettext_lazy(
            "profile.lang.estonian", "Estonian")
        PERSIAN = "persian", pgettext_lazy("profile.lang.persian", "Persian")
        AFRIKAANS = "afrikaans", pgettext_lazy(
            "profile.lang.afrikaans", "Afrikaans")
        SWAHILI = "swahili", pgettext_lazy("profile.lang.swahili", "Swahili")

    image_type = models.CharField(
        choices=LanguageChoices.choices,
        default=LanguageChoices.ENGLISH,
        max_length=255)

    participants = models.ManyToManyField(
        User, related_name='project_participants', null=True, blank=True)

    users_connected = models.ManyToManyField(
        User, related_name='project_users_connected', null=True, blank=True)


class ChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='project_messages')

    original_message = models.TextField()
    data = models.JSONField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='message_user')
