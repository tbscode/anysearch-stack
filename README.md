# Anychat ( our tum.ai hackathon submission )

Anychat the first ai supportet multi-lingual group chat for project works planning and reports!

## some of the sills

Currently deployed at [`anychat.t1m.me`](https://anychat.t1m.me)

You can login with the test user: `testUser1`, pw: `Test123!`
And If you want to test the peer to peer chat you can login with any of `testUser<ID>` for ids in 1-20.

Send a chat message and see it appear in all connected user chat with translations in all languages.
Want to ask a topic spcific question just chat with the project ai `@ai ...`

- fully scalable production ready kubernetes deployment, that can be run completely locally in development
- micro service contain architecture
- custom django channels redis implementation for manging multiple project groups and distribting messages to connected users
- fully websocket enabled group chat
- topic specific ai assistant in any group chat, just start you message with `@ai ...`
- intelligent ai agent that can device when to use specic tools and is customizable with multiple tools
- agent implementation is based on langchain and support _ANY_ LLM as base, so we can deploy our own model in the future or switch the api whenever we want
- the ai has internet access, one of the tools is that the ai can decide when to lookup something in the internet
- autmatic translation in _ALL_ languages of a projects participants: everybody can send messages in their choosen language and still read everything!
- chat is fully file supportet send images or other attachments!
- intelligent attachment processing, automatic image content annotation and voice message to text
- loging screen and admin user management comes packages and ready
- automatic api doc and shema generation, fully typed api serializers

# The stack

The anychat stack Stack is a production-ready Kubernetes deployment for building dynamic web applications. It includes a Django backend and a React + Next.js frontend.

This project is uses [`Tim's Stack`](https://github.com/tbscode/tiny-django).

## Prerequisites

- `make` is required for managing the commands.
- `Docker` is required for local development.

## Backend

The backend is a Django application with various pre-installed packages and addons.

- Build the development backend: `make backend_build`
- Start the development backend: `make backend_run`

The server will start and be exposed at port 8000. Note that you cannot access `localhost:8000/` without the Next.js frontend container. However, you can visit the admin dashboard at `localhost:8000/admin/` and the API documentation at `localhost:8000/api/schema/redoc/`.

In development, the `./back` folder is mounted into the container for hot reloading.

## Frontend

The frontend uses Next.js with some pre-built components and pages. A global state is set up for all pages containing the data provided by the Django backend.

The `./front` folder is mounted into the container for hot reloading during development.

- Build the frontend container: `make frontend_build`
- Start the frontend container: `make frontend_run`

The frontend can overwrite any page path except `/api`, `/admin`, `/static`, and `/media`. This allows you to configure your `pages` as needed.

`daisyui` & `tailwindcss` are also set up for the frontend.

To ensure that Next.js pages are hydrated with the backend data from the Django container, access the frontend through `localhost:8000/` instead of `localhost:3000/`. Pages should be developed to work both with and without backend data.

## Kubernetes

You can also build a replica for the production build or fully develop in kubernetes locally!
I recommend `microk8s` for a quick mininmal but complete kubernetes dist.

Use `make microk8s_setup` to prepare the local `microk8s` setup.

Use `make frontend_build_push` and `make backend_build_push` to build frontend and backend container images and push then to the local registry which was initalized in the setup.

Now you can install the helm chart with `make helm_install`, check that all deployments and servies are running with `make microk8s_status` and check the running pages at local host http port 80 by vising plain `localhost`.

```
this stack was provided by Tim Schupp, (Tim Benjamin Software)
tim@timschupp.de
t1m.me
(C) `README.md`, `helm-chart/*`, `back/*`
```
