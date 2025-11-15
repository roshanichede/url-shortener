from django.shortcuts import render
from django.db import models
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .supabase_client import supabase
from django.shortcuts import redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def dashboard(request):
   return render(request,'index.html')

@csrf_exempt
def urlshortener(request):
   if request.method == 'POST':
      raw_body = request.body
      try:
         decoded_body = raw_body.decode('utf-8')
         data = json.loads(decoded_body)
         short_code = str(uuid.uuid4())[:8]  # Generate a short code
         original_url = data.get('url')
         
         val = URLValidator()
         try:
            val(original_url)
         except ValidationError:
            return HttpResponseBadRequest("Oops! That doesn’t look like a real URL")
         
         if not original_url or len(original_url.strip())==0:
            return HttpResponse("Oops! you forgot the main character: the URL \n(Missing 'url' in request body)")

         if not (original_url.startswith('http://')) or (original_url.startswith('https://')):
            original_url = 'https://' + original_url
         
         blocked_urls = (
            "http://localhost",
            "http://127.",
            "http://10.",
            "http://192.168",
            "file://",
            "ftp://",
            "data:",
            "javascript:")
         
         if original_url.startswith(blocked_urls):
            return HttpResponseBadRequest("This URL is giving danger zone energy!!")
     
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
   return JsonResponse({'error': 'Method not allowed'}, status=405)

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