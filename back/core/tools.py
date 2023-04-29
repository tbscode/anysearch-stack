from core.models import User, Project, ChatMessage
import json
from django.conf import settings
from core.models import get_random_language, translate_to_all_langs_in_list, get_langs_in_project


def get_or_create_base_admin():
    user = User.objects.filter(username=settings.BASE_ADMIN_USERNAME)
    if not user.exists():
        user = User.objects.create_superuser(
            username=settings.BASE_ADMIN_USERNAME,
            password=settings.BASE_ADMIN_USER_PASSWORD
        )
    return user


def create_simple_user_setup():
    # creates some projects, and some users for these
    users = []

    for i in range(20):
        user = User.objects.create("Test123!", username=f"testUser{i}")
        user.profile.language = get_random_language()
        user.profile.save()
        users.append(user)

    project_cutoff = 10

    project1 = Project.objects.create(
        name="Ceiling of mister maier",
        description="Building the ceiling of mister maier",
    )

    # add the first project_cutoff user to project1
    for user in users[:project_cutoff + 5]:
        project1.participants.add(user)
        user.projects.add(project1)
        user.save()

    project2 = Project.objects.create(
        name="Terasse von jeniffer lawrence",
        description="Yeah yuhi jippie",
    )

    for user in users[project_cutoff:]:
        project2.participants.add(user)
        user.projects.add(project2)
        user.save()

    # we do also add an AI user to eact of the projects
    # TODO: these ai users should be added automaticly in the future
    ai1 = User.objects.create("AiTest123!", username=f"AI1")
    ai2 = User.objects.create("AiTest123!", username=f"AI2")
    project1.participants.add(ai1)
    project2.participants.add(ai2)

    ai1.projects.add(project1)
    ai2.projects.add(project2)
    project1.ai_user = ai1
    project2.ai_user = ai2
    ai1.save()
    ai2.save()

    # generate some random messages here
    languages_p1 = get_langs_in_project(project1)
    languages_p2 = get_langs_in_project(project2)
    print("L1", languages_p1)
    print("L2", languages_p2)

    for i in range(50):
        random_user = users[i % project_cutoff]
        message = f"Hello, this is a test message {i}"
        data = translate_to_all_langs_in_list(
            message, languages_p1, random_user.profile.language)
        print("DATA", data)
        ChatMessage.objects.create(
            original_message=message,
            sender=random_user,
            project=project1,
            data=data
        )

    project1.save()
    project2.save()
