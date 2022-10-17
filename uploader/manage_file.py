import pandas as pd
import logging
from django.http import JsonResponse
from cliente.models import Cliente
from producto.models import Producto
from sucursal.models import Sucursal
from sqlalchemy import create_engine
from inventario.models import Inventario


logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} {levelname:<8} {message}",
    style='{',
    filename='log.log',
    filemode='w'
    )

database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format( user='postgres',password='qwertyui',database_name='nexos',)
engine = create_engine(database_url, echo=False)

def manage_file_pd(file):
    try:
        df = pd.read_csv(file)
        logging.info('Start reading file')
        FechaInventario = df['FechaInventario']
        GLN_Cliente = df['GLN_Cliente']
        GLN_Sucursal = df['GLN_Sucursal']
        Gtin_Producto = df['Gtin_Producto']
        Inventario_Final = df['Inventario_Final']
        PrecioUnidad = df['PrecioUnidad']
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
        rename_inventario = inventario.rename(columns={'GLN_Sucursal': 'GLN_sucursal_id'})
        insert_inventario = rename_inventario.to_sql(Inventario._meta.db_table, if_exists='append', con=engine, index=False)
        print('*'*100)
        print(type(insert_inventario))
        if not insert_inventario:
            report_failed_insert('inventario')

            return JsonResponse({
                    'ok': 'file is saved'
                })
    except Exception:
        return JsonResponse({
                'error': 'some error'
            })

def report_failed_insert(name_table):
    logging.info('error to insert in '+name_table)
    return JsonResponse({
            'error': 'error to insert in '+name_table
        })