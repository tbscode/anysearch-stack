from django.conf import settings
import requests
from django.http import HttpResponse


def index(request, path):
    return render_nextjs_page({"test": "test"}, path=path)


def render_nextjs_page(data, path=""):
    url = settings.NEXTJS_HOST_URL
    resp = requests.post(f"{url}/{path}", json=data)
    return HttpResponse(resp.text)
