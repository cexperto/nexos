from turtle import pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
import logging

from .manage_file import manage_file_pd
from .file_azure import upload_file_to_blob


ALLOWED_EXTENTIONS = ['text/csv']

def index(request):
    return JsonResponse({
            'ok': 'welcom nexos API'
        })

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} {levelname:<8} {message}",
    style='{',
    filename='log.log',
    filemode='w'
    )



@csrf_exempt
def upload_file(request):
    file = request.FILES['file']
    if file.content_type not in ALLOWED_EXTENTIONS:
        logging.info('format file is not valid')
        return JsonResponse({
            'error': 'file is not csv'
        })
    upload_file_to_blob(file)
    return manage_file_pd(file)