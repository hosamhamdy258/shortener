from django.urls import path

from shortener.views import shortener

app_name = "shortener"
urlpatterns = [
    # path("", index),
    # path("<str:short_url>/", redirect_view),
    path("<str:short_url>/", shortener),
    path("", shortener),
]
