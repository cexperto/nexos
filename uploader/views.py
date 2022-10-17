from turtle import pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from numpy import insert, product
from sqlalchemy import create_engine
from cliente.models import Cliente
from producto.models import Producto
from sucursal.models import Sucursal
from inventario.models import Inventario
import logging
# from azure.storage.blob import BlobClient
# from django.conf import settings
import pandas as pd

database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format( user='postgres',password='qwertyui',database_name='nexos',)
engine = create_engine(database_url, echo=False)

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

def report_failed_insert(name_table):
    logging.info('error to insert in '+name_table)
    return JsonResponse({
            'error': 'error to insert in '+name_table
        })

@csrf_exempt
def upload_file(request):
    file = request.FILES['file']
    if file.content_type not in ALLOWED_EXTENTIONS:
        logging.info('format file is not valid')
        return JsonResponse({
            'error': 'file is not csv'
        })

    df = pd.read_csv(file)
    logging.info('Start reading file')
    FechaInventario = df['FechaInventario']
    GLN_Cliente = df['GLN_Cliente'].to_frame()
    GLN_Sucursal = df['GLN_Sucursal'].to_frame()
    Gtin_Producto = df['Gtin_Producto'].to_frame()
    Inventario_Final = df['Inventario_Final'].to_frame()
    PrecioUnidad = df['PrecioUnidad'].to_frame()
    logging.info('file ready for upload')
    insert_cliente = GLN_Cliente.to_sql(Cliente._meta.db_table, if_exists='append', con=engine, index=False)
    if not insert_cliente:
        report_failed_insert('cliente')
    products = pd.concat([Gtin_Producto, PrecioUnidad, GLN_Cliente], axis=1, join="inner")
    rename_products = products.rename(columns={'GLN_Cliente': 'GLN_Cliente_id'})
    insert_products = rename_products.to_sql(Producto._meta.db_table, if_exists='append', con=engine, index=False)
    if not insert_products:
        report_failed_insert('producto')
    sucursal = pd.concat([GLN_Sucursal, Gtin_Producto], axis=1, join="inner")
    rename_sucursal = sucursal.rename(columns={'Gtin_Producto': 'Gtin_Producto_fk_id'})
    insert_sucursal = rename_sucursal.to_sql(Sucursal._meta.db_table, if_exists='append', con=engine, index=False)
    if not insert_sucursal:
        report_failed_insert('sucursal')
    inventario = pd.concat([FechaInventario, Inventario_Final, GLN_Sucursal], axis=1, join="inner")
    rename_inventario = inventario.rename(columns={'GLN_Sucursal': 'GLN_Sucursal_id'})
    insert_inventario = rename_inventario.to_sql(Inventario._meta.db_table, if_exists='append', con=engine, index=False)
    if not insert_inventario:
        report_failed_insert('inventario')

    JsonResponse({
            'ok': 'file is saved'
        })