# Anysearch Stack

Anysearch Stack is a production-ready Kubernetes deployment for building dynamic web applications. It includes a Django backend and a React + Next.js frontend.

This project is a fork of [Tim's Stack](https://github.com/tbscode/tiny-django).

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
