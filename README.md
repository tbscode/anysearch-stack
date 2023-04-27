### k8s-django-nextjs

Tim's stack. A fully scalabe django (microservices), nextjs (frontend), kubernetes stack.

Some cool skills:

- production / staging / development setup consistency
- everything fully containerized
- ONLY stystem requirement `microk8s`
- automatic code & api documentation for django backend
- full nextjs ssr compatability
- host path mounts still allow live editing with hot reloads in development

The django backend comes packed with a lot of convenient tooling.
The combination of `django-nextjs` and custom `microk8s` routing allowes the backend to dynamicly request pre-rendered pages from next-js, django may also dynamicly pass data to any nextjs page, allowing SSR even for dynamic pages.

The combination of `rest_framework` and `djangorestframework-dataclasses` allowes to quickly and consisely write RESTFULL apis, rate limiting, token autorization etc always available.

Based on automatic dataclass based serializers from `restframework-dataclasses` we can use `drf-spectacular[sidecar]` to generate and render full openapi documentations.

### setup / development

1. install `microk8s` [instuctions mac / linux], [instuctions windows]
2. enable services `microk8s enable helm ingress dns registry`
3. start kubernetes `microk8s start`
4. Install the helm chart in dev-mode `microk8s helm install --dry-run --debug ./helm-chart/ --generate-name --set rootDir=$(pwd)`
5. Check that the servies are running

When you stop developing simply do `microk8s stop` and `microk8s start` to continue.
Local development will automaticly mount directorys `back`, `front` for hot code reloading.

Appart from that an serveral smaller differences like cert-manager, container-secrets, etc. , are production and development environments identical.

#### Build images

for development

```bash
docker build -f Dockerfile.back_dev back
docker build -f Dockerfile.front_dev front

```

#### convenience mappings

`alias helm="microk8s helm"`
`alias kubectl="microk8s kubectl"`

### Usage

helm chart changed: `microk8s helm install --dry-run --debug ./helm-chart/ --generate-name`
