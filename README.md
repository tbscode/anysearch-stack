### anysearch stack

a complete production ready kubernetes deployment for building dynamic web apps.

Includes a django backend and a react + nextjs frontend.

> this is a fork of [`Tim's Stack`](https://github.com/tbscode/tiny-django)

### the stack

The commands are currently managed with `make` so this is a requirement if you dont want to copy paste.
Also the local development can be done completely using `docker` so thats a requirement.

The backend can dynamicly send request to the nextjs container with dynamic page data, nextjs then returns the rendered html & javascript which is then served to the client.

For all the following make commands if you wonder what they do just checkout the `--dry-run` & the `Makefile`.

#### the backend

The backend is a dockerized django application with a buch of neat packages and addons pre installed.

You can build the development backend via `make backend_build`.

Start the development backend via `make backend_run` now you should see the server started and exposed at port 8000.

Note that you will not be able to visit `localhost:8000/` cause this requires the nextjs frontend container.
You can however checkt that the admin dashboard is up at `localhost:8000/admin/` or that the api documentation is generated at `localhost:8000/api/schema/redoc/`.

In development we will mount the `./back` folder into the container so code changes are hot reloaded.

#### the frontend

The frontend spins up a simple nextjs container with some components and pages. We setup a global state for all pages that contains the data set by the django backend when requesting a rendered page.

Also in development we mount the `./front` folder into the container for hot reloads.

Use `make frontend_build` to build the frontend container, use `make frontend_run` to start it.

The frontend may overwite any page path except `/api`, `/admin`, `/static` and `/media`, so you can configure you `pages` as you want.

We also have `daisyui` & `tailwindcss` setup for the frontend.

If you have both backend and frontend container running you should also acess the frontend via `localhost:8000/` and not via `localhost:3000/` so that the nextjs pages are hidated with the backend data from the django container. But we should always dynamicly develop pages to also work without backend data!
