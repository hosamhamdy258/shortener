import json
import secrets
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from shortener.models import Shortener


@csrf_exempt
def shortener(request, short_url=None):
    if request.method == "GET":
        if short_url:
            obj = get_object_or_404(Shortener, short_url=short_url)
            return redirect(obj.target_url)
        return render(request, "shortener/index.html")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            target_url = data.get("url")
            if not target_url:
                return JsonResponse({"message": _("URL is required")}, status=400)

            validate = URLValidator()
            try:
                validate(target_url)
            except ValidationError:
                return JsonResponse({"message": _("Invalid URL format")}, status=400)

            obj, created = Shortener.objects.get_or_create(target_url=target_url, defaults={"short_url": generate_unique_short_url(5)})
            return JsonResponse({"message": obj.short_url}, status=201 if created else 200)

        except json.JSONDecodeError:
            return JsonResponse({"message": _("Invalid JSON")}, status=400)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": _("POST request required")}, status=405)


RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_random_string(length, allowed_chars=RANDOM_STRING_CHARS):
    """
    Return a securely generated random string.
    """
    return "".join(secrets.choice(allowed_chars) for i in range(length))


def generate_unique_short_url(length):
    while True:
        generated_url = get_random_string(length)
        if not Shortener.objects.filter(short_url=generated_url).exists():
            return generated_url
