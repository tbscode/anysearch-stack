from django.conf import settings
import requests
from django.http import HttpResponse
from core.api.user_data import get_user_data


def index(request, path):
    if request.user.is_authenticated:
        return render_nextjs_page(get_user_data(request.user), path=path)
    return render_nextjs_page({"test": "test"}, path=path)


def render_nextjs_page(data, path=""):
    url = settings.NEXTJS_HOST_URL
    resp = requests.post(f"{url}/{path}", json=data)
    return HttpResponse(resp.text)
