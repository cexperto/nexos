from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
import uuid
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
# from azure.storage.blob import BlobClient
from django.conf import settings



ALLOWED_EXTENTIONS = ['text/csv']

def index(request):
    return JsonResponse({
            'ok': 'welcom nexos API'
        })

@csrf_exempt
def upload_file(request):
    file = request.FILES['file']
    if file.content_type not in ALLOWED_EXTENTIONS:
        return JsonResponse({
            'error': 'file is not csv'
        })
    return HttpResponse(file)