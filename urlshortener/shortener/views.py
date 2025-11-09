from django.shortcuts import render
from django.db import models
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .supabase_client import supabase
from django.shortcuts import redirect

@csrf_exempt
def dashboard(request):
   return render(request,'index.html')

def urlshortener(request):
   if request.method == 'POST':
      raw_body = request.body
      try:
         decoded_body = raw_body.decode('utf-8')
         data = json.loads(decoded_body)
         short_code = str(uuid.uuid4())[:8]  # Generate a short code
         original_url = data.get('url')
         
         if not original_url:
            return HttpResponseBadRequest("Missing 'url' in request body")

         if original_url.startswith('http://') is False and original_url.startswith('https://') is False:
            original_url = 'https://' + original_url
         
         res = {
            "original_url": original_url,
            "short_code": short_code
         }
         
         supabase.table("urlshortener").insert(res).execute()
         return JsonResponse(res, status=200)
      except json.JSONDecodeError:
         return HttpResponse("Invalid JSON in request body", status=400)
      except UnicodeDecodeError:
         return HttpResponse("Could not decode request body", status=400)
   return render(request,'index.html')

def geturl(request, short_code):
   if request.method == 'GET':
      try:
         res = supabase.table("urlshortener").select("original_url").eq("short_code", short_code).execute()
         original_url = res.data[0]['original_url']
         print(f'hello {res.data[0]['original_url']}')
         
         if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url
            
         return redirect(original_url)
      except json.JSONDecodeError:
         return HttpResponse("Invalid JSON in request body", status=400)
      except UnicodeDecodeError:
         return HttpResponse("Could not decode request body", status=400)
   return render(request,'index.html')