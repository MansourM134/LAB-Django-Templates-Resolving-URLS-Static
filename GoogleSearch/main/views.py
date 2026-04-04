from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import json
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent / 'content'

# Create your views here.

def home_view(request:HttpRequest):

    return render(request, "main/home.html")

def terms_view(request:HttpRequest):
    
    context = json.loads((CONTENT_DIR / 'terms.json').read_text(encoding='utf-8'))

    return render(request, "main/terms.html", context)
