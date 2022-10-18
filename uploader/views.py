"""
for save file in blog storage uncomment line 13 and 42, but make sure have credentials
follow this video for have credentials if is the case https://www.youtube.com/watch?v=PjOjrIZOetM
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import logging

from cliente.models import Cliente
from .manage_file import manage_file_pd
# from .file_azure import upload_file_to_blob


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
    logging.info('data is saved in postgresDB')
    # upload_file_to_blob(file)
    # logging.info('data is saved in blob')    
    return manage_file_pd(file)


@csrf_exempt
def query_client(request):
    try:
        query_client=Cliente.objects.select_related('GLN_Cliente','producto').values_list('GLN_Cliente','producto')    
        return JsonResponse({'data': list(query_client)})
    except Exception:
        return JsonResponse({'error': 'no data found'})
