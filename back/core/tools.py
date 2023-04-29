from core.models import User, Project, ChatMessage
import json
from django.conf import settings
from core.models import get_random_language, translate_to_all_langs_in_list, get_langs_in_project
from random import randint


def get_or_create_base_admin():
    user = User.objects.filter(username=settings.BASE_ADMIN_USERNAME)
    if not user.exists():
        user = User.objects.create_superuser(
            username=settings.BASE_ADMIN_USERNAME,
            password=settings.BASE_ADMIN_USER_PASSWORD
        )
    return user


chat_messages_history_2 = [
    "As a gardener on this construction project, I was tasked with the job of preparing the soil for the new garden beds. It was a hot summer day and the work was demanding, but I took pride in doing it right. The first step was to remove any debris or unwanted vegetation from the site. Once the site was cleared, we brought in a rototiller to break up the soil and loosen it up for planting.",
    "Next, I worked on creating new garden beds. I dug out trenches for the raised beds and filled them with a rich, organic soil mix. The garden beds were then carefully planted with a variety of flowers, vegetables, and herbs. It was rewarding to see the transformation of the site as the garden began to take shape.",
    "The electricians had their own challenges as they worked to install lighting throughout the garden. They had to ensure that the wiring was properly installed and that all the lights were connected to the power source. They also had to work around the gardeners and plumbers who were busy doing their own work.",
    "The plumbers were responsible for installing a new irrigation system to keep the garden watered. They had to run pipes throughout the garden and install sprinkler heads in each garden bed. It was a complicated process, but they managed to get it done efficiently.",
    "Meanwhile, the heavy construction equipment was hard at work in the background. The bulldozers and excavators were used to level the ground and prepare it for the new garden. They also helped to transport heavy materials like soil and paving stones around the site.",
    "As the project came to a close, we all felt a sense of pride in what we had accomplished. The garden was now a beautiful oasis, complete with flowers, vegetables, and a new irrigation system. It was a job well done and we were happy to have been a part of it."
]

chat_messages_history_1 = [
    "Hey guys, have you heard about the plan to install an outdoor lighting system around the office building?",
    "Yes, I think it's a great idea. It would really improve the overall security and appearance of the premises.",
    "I agree, it would also make it safer for us when we leave work late in the evenings. So, have they decided on the type of lighting system to be installed?",
    "I'm not sure about the details yet, but I believe they're considering LED lights as they are energy-efficient and have a longer lifespan.",
    "That's a smart choice. LED lights are not only cost-effective but also environmentally friendly. Do we know if they plan to install motion sensor lights as well?",
    "I think that's a possibility. It would make sense to have motion sensor lights in certain areas, like the parking lot and walkways, to save energy.",
    "Absolutely. Plus, motion sensor lights can also act as a deterrent for any potential intruders.",
    "True. Do we have any idea about the timeline for this project? When are they planning to start the installation?",
    "I heard that they want to start the installation within the next couple of weeks and aim to complete it within a month.",
    "That's a pretty tight schedule. I hope they've hired a professional company to ensure the installation is done properly.",
    "Yes, they have. The company they've chosen has a great reputation and years of experience in outdoor lighting installations.",
    "That's good to hear. I'm sure they'll do a great job. Are we expecting any disruptions during the installation process?",
    "There might be some minor disruptions, especially in the parking areas, but the company will try to minimize the impact on our daily operations.",
    "I guess we'll just have to be a little flexible and patient during the installation process.",
    "Agreed. I'm sure it'll be worth it once everything is up and running.",
    "Definitely. The new lighting system will not only make our workplace safer and more secure but also enhance the overall aesthetics of the building.",
    "Yes, and it'll be a great addition to the company's efforts in promoting an eco-friendly work environment.",
    "I'm looking forward to seeing the final result. Let's hope the installation goes smoothly and without any major issues.",
    "Fingers crossed. I'll keep you guys updated if I hear any more information about the project.",
    "Sounds good. Thanks for keeping us in the loop!",
    "Yeah, thanks! Can't wait to see the new lighting system in action."
]

default_projects = [
    "Installation of outdoor lighting system",
    "Installation of irrigation system"
]


def create_simple_user_setup():

    # creates some projects, and some users for these
    users = []

    for i in range(20):
        user = User.objects.create("Test123!", username=f"testUser{i}")

        pic_url = f"/_nstat/real-humans/{i}.jpg"
        user.profile.language = get_random_language()
        user.profile.image = pic_url
        user.profile.save()
        users.append(user)

    project_cutoff = 10

    project1 = Project.objects.create(
        name=default_projects[0],
        description="Building the ceiling of mister maier",
    )

    # add the first project_cutoff user to project1
    for user in users:
        project1.participants.add(user)
        user.projects.add(project1)
        user.save()

    project2 = Project.objects.create(
        name=default_projects[1],
        description="Yeah yuhi jippie",
    )

    for user in users:
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

    i = 0
    for msg in chat_messages_history_1:
        random_user = users[randint(0, len(users) - 1)]
        i += 1
        data = translate_to_all_langs_in_list(
            msg, languages_p1, random_user.profile.language)
        print("DATA", data)
        ChatMessage.objects.create(
            original_message=msg,
            sender=random_user,
            project=project1,
            data=data
        )

    i = 0
    for msg in chat_messages_history_2:
        random_user = users[randint(0, len(users) - 1)]
        i += 1
        data = translate_to_all_langs_in_list(
            msg, languages_p2, random_user.profile.language)
        print("DATA", data)
        ChatMessage.objects.create(
            original_message=msg,
            sender=random_user,
            project=project2,
            data=data
        )

    project1.save()
    project2.save()
