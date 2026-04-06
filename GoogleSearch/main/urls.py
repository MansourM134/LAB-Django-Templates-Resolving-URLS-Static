from django.urls import path
from . import views

app_name = "main"

SUPPORTED_LANGS = {"en", "ar"}

urlpatterns = [

    path("", views.home_view, name="home_view"),
    path("search/", views.search_view, name="search_view"),
    path("set-theme/", views.set_theme_view, name="set_theme_view"),
    path("terms/<str:lang>/", views.terms_view, name="terms_view"),
    path("terms/", views.terms_redirect_view, name="terms_redirect_view"),

]