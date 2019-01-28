from django.conf import settings
from django.utils import timezone

from .models import (
    Transaction, ServerResponse
)
from background_task import background

import requests, json
import datetime


# Check Status Product
def get_status_productrb(prod_code):
    _url = settings.RB_URL
    _uid = settings.RB_UID
    _key = settings.RB_KEY

    payload = {
        "method"      : "rajabiller.info_produk",
        "uid"         : _uid,
        "pin"         : _key,
        "kode_produk" : prod_code,
    }

    try :
        r = requests.post(url=_url, data=json.dumps(payload), timeout=15)
        if r.status_code == requests.codes.ok:
            rson = r.json()
            # {'STATUS': '00', 'UID': 'SP118171', 'HARGA': '10400', 'PIN': '------', 'KET': 'SUKSES', 'KODE_PRODUK': 'S10H', 'ADMIN': '0', 'STATUS_PRODUK': 'AKTIF', 'KOMISI': '0'}

        r.raise_for_status()
        
    except:
        rson = dict()

    return rson


# H2H Rajabiller
@background(schedule=1)
def h2h_rbserver(trx_id):
    server_res_obj = ServerResponse.objects.get(trx_id=trx_id)
    trx = server_res_obj.trx

    _url = settings.RB_URL
    _uid = settings.RB_UID
    _key = settings.RB_KEY

    # Check Status Product H2H
    # rb_product = get_status_productrb(trx.product_code)


    # Starting Transaction H2H
    payload = {
        "method"      : "rajabiller.pulsa",
        "uid"         : _uid,
        "pin"         : _key,
        "no_hp"       : trx.customer,
        "kode_produk" : trx.product_code,
        "ref1"        : trx.trx_code,
    }
    prod_group = trx.product.group.slug

    if prod_group not in ['pulsa', 'data']:
        payload['method'] = "rajabiller.game"

    try:
        r = requests.post(url=_url, data=json.dumps(payload), timeout=10)
        if r.status_code == requests.codes.ok:
            rson = r.json()
        
        r.raise_for_status()

        server_res_obj.kode_produk = rson.get('KODE_PRODUK','')
        server_res_obj.waktu = rson.get('WAKTU','')
        server_res_obj.no_hp = rson.get('NO_HP','')
        server_res_obj.sn = int(rson.get('SN',0))
        server_res_obj.nominal = rson.get('NOMINAL','')
        server_res_obj.ref1 = rson.get('REF1','')
        server_res_obj.ref2 = rson.get('REF2','')
        server_res_obj.status = rson.get('STATUS','')
        server_res_obj.ket = rson.get('KET','')
        server_res_obj.saldo_terpotong = int(rson.get('SALDO_TERPOTONG',0))
        server_res_obj.sisa_saldo = int(rson.get('SISA_SALDO',0))
        server_res_obj.save()

        # Update Status Transaction to In Process
        trx.status = 'PR'
        trx.save()

    except:
        pass


# Check Status Transaction H2H
@background(schedule=60)
def get_status_rbserver(trx_id):
    trx_objs = Transaction.objects.filter(
        pk=trx_id, status_in=['OP', 'PR']
    )
    if trx_objs.exists():
        get_trx = trx_objs.get()

        res_obj = ServerResponse.objects.get(trx=get_trx)
        
        # Validation if ref2 filled  
        if res_obj.ref2 is not None and res_obj.ref2 != '':
            _url = settings.RB_URL
            _uid = settings.RB_UID
            _key = settings.RB_KEY

            h_tgl = timezone.localtime(get_trx.due_date) + datetime.timedelta(hours=1)
            l_tgl = tgl1 + datetime.timedelta(days=-1)

            payload = {
                "method"      : "rajabiller.datatransaksi",
                "uid"         : _uid,
                "pin"         : _key,
                "tgl1"        : l_tgl.strftime('%Y%m%d%H%M%S'),
                "tgl2"        : h_tgl.strftime('%Y%m%d%H%M%S'),
                "id_transaksi": res_obj.ref2,
                "id_produk"   : "",
                "idpel"       : "",
                "limit"       : ""
            }

            try :
                r = requests.post(url=_url, data=json.dumps(payload), timeout=15)
                if r.status_code == requests.codes.ok:
                    rson = r.json()

                r.raise_for_status()
            except:
                pass

            try :
                data = rson['RESULT_TRANSAKSI'][0]
                # '1243054045#20190116133742#S100H#TELKOMSEL SIMPATI / AS 100RB#081282100202#00#SUCCESS#96825#41003271424010#SUKSES'
                ref_id, waktu, prodcode, prod, hp, status, ket, price, sn = data.split('#', 8)
                if status == '00':
                    if sn is not null and sn != '':
                        # Success
                        res_obj.sn = sn
                        res_obj.status = status
                        res_obj.saldo_terpotong = int(price)
                        res_obj.save()

                        get_trx.status = 'CO'
                        get_trx.save(update_fields=['status'])

                elif status in ['', '68']:
                    # In process
                    pass

                else :
                    # Failed
                    res_obj.status = status
                    res_obj.save()

                    get_trx.status = 'FL'
                    get_trx.save(update_fields=['status'])

            except:
                pass