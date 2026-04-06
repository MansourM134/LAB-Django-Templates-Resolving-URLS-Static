from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
#from django.utils.translation import get_language
from django.urls import reverse
from django.utils import translation
from urllib.parse import urlencode
import json
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent / 'content'
SUPPORTED_LANGS = {'en', 'ar'}
DEFAULT_LANG = 'en'
GOOGLE_SEARCH_URL = 'https://www.google.com/search'

# Create your views here.

def home_view(request:HttpRequest):

    return render(request, "main/home.html")

def search_view(request: HttpRequest):
    """
    Receive the search form's GET submission then validate the query
    and redirect to Google Search.
    """
    query = request.GET.get('q', '').strip()

    if not query:
        # Re-render the home page with an error flag instead of hitting Google
        return render(request, 'main/home.html', {'search_error': True})

    params = {'q': query}

    if request.GET.get('btnI'):
        params['btnI'] = request.GET['btnI']

    return redirect(f'{GOOGLE_SEARCH_URL}?{urlencode(params)}')

def terms_redirect_view(request: HttpRequest):
    """Redirect to the default language version."""
    return redirect(reverse('main:terms_view', kwargs={'lang': DEFAULT_LANG}))

def terms_view(request:HttpRequest, lang:str):
    '''to choose which json to load by language'''
    #only takes supported languags
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG


    content_file = CONTENT_DIR / f'terms.{lang}.json'

    #if the user language doesnt exist go back to english
    if not content_file.exists():
        content_file = CONTENT_DIR / 'terms.en.json' 

    
    context = json.loads(content_file.read_text(encoding='utf-8'))
    context['current_lang'] = lang

    #debug
    print("LANG:", lang)
    print("FILE:", content_file)

    return render(request, 'main/terms.html', context)

def theme(request):
    current_theme = request.COOKIES.get('theme', 'light')
    if current_theme not in ('light', 'dark'):
        current_theme = 'light'
    return {'theme': current_theme}

def set_theme_view(request: HttpRequest):

    if request.method != 'POST':
        return redirect(reverse('main:home_view'))

    new_theme = request.POST.get('theme', 'light')

    redirect_to = request.POST.get('next', '/')
    response = redirect(redirect_to)

    response.set_cookie(
        key='theme',
        value=new_theme,
        max_age=60 * 60 * 24 * 365,
    )

    return response
