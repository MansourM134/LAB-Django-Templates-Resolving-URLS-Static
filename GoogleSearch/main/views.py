from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.utils.translation import get_language
import json
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent / 'content'

# Create your views here.

def home_view(request:HttpRequest):

    return render(request, "main/home.html")

def terms_view(request:HttpRequest):
    lang = get_language() or 'en'
    lang_code = lang.split('-')[0]

    content_file = CONTENT_DIR / f'terms.{lang_code}.json'

    #if the user language doesnt exect go back to english
    if not content_file.exists():
        content_file = CONTENT_DIR / 'terms.en.json' 

    
    context = json.loads(content_file.read_text(encoding='utf-8'))
    
    return render(request, 'main/terms.html', context)
