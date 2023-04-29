from channels.generic.websocket import AsyncWebsocketConsumer
import json
from core.api.handle_message import handle_socket_message
from asgiref.sync import sync_to_async


def get_user_prodjects(user, connect_user_to_project=True):
    # loop through all user prodjects
    project_hashes = []

    for project in user.projects.all():
        if connect_user_to_project:
            # add the user as connecte to the project
            project.users_connected.add(user)
            project.save()
        project_hashes.append(str(project.hash))
    return project_hashes


def remove_users_from_project(user):
    for project in user.projects.all():
        project.users_connected.remove(user)
        project.save()


def get_connected_users_per_project(user):
    data = {}

    for project in user.projects.all():
        data[str(project.hash)] = [str(user.hash)
                                   for user in project.users_connected.all()]
    return data


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("CONNECT ATTEMPTED")

        if self.scope["user"].is_anonymous:
            # only allow already authenticated users
            await self.close()
        else:
            print("USERNAME", self.scope["user"].username)
            user = self.scope["user"]

            await self.channel_layer.group_add(f"user-{user.hash}", self.channel_name)
            await self.accept()

            # so all users per default connect to the websocket
            # but now we need to check which prodject the user belongs to
            # For all theses prodjects we need to add them to different group
            projects = await sync_to_async(get_user_prodjects)(user, True)
            connected_usrs_per_project = await sync_to_async(get_connected_users_per_project)(user)
            for project in projects:
                project_group_slug = f"project-{project}"
                await self.channel_layer.group_add(project_group_slug, self.channel_name)

                # Now we notify all channels that that user went online!
                await self.channel_layer.group_send(project_group_slug, {
                    "type": "broadcast_message",
                    "data": {
                        "event": "user_joined",
                        "user": {
                            "hash": str(user.hash),
                            "name": user.first_name
                        }
                    }
                })

            # we tell the user that he sucessfully connected
            # then we also thell him which user is connected to which channel
            await self.send(text_data=json.dumps({
                "event": "user_connected",
                "channel": str(user.hash),
                "projects": connected_usrs_per_project
            }))

    async def broadcast_message(self, event):
        # Sends a message to *all* random call connected users
        # But it doesn't forward the messsage to the user that has triggered the event
        # e.g.: update amount random users
        if self.scope["user"].is_anonymous:
            # only allow already authenticated users
            await self.close()
        else:
            await self.send(text_data=json.dumps({
                # as convention 'data' should always contain a 'event'
                **event['data'],
            }))

    async def receive(self, text_data):
        if self.scope["user"].is_anonymous:
            # only allow already authenticated users
            await self.close()
        else:
            print("RECEIVED MESSAGE", text_data)
            data = await sync_to_async(json.loads)(text_data)
            resp = await sync_to_async(handle_socket_message)(data, self.scope["user"])

    async def disconnect(self, close_code):

        if self.scope["user"].is_anonymous:
            # only allow already authenticated users :D
            await self.close()
        else:
            user = self.scope["user"]

            await sync_to_async(remove_users_from_project)(user)
            projects = await sync_to_async(get_user_prodjects)(user, False)

            for project in projects:
                project_group_slug = f"project-{project}"
                # Now we notify all channels that that user went offline
                await self.channel_layer.group_send(project_group_slug, {
                    "type": "broadcast_message",
                    "data": {
                        "event": "user_left",
                        "user": {
                            "hash": str(user.hash),
                            "name": user.first_name
                        }
                    }
                })

            # cool that should be the connect / disonnect logic done!
