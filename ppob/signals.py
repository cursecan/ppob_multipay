from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import (
    Transaction, 
    InqueryResponse, PaymentResponse
)
from bill.models import (
    Billing, Profit
)

import requests, json

@receiver(post_save, sender=Transaction)
def transaction_trigering(sender, instance, created, **kwargs):
    _url = settings.RB_URL
    _uid = settings.RB_UID
    _key = settings.RB_KEY

    server_group = instance.product.group.slug
    product = instance.product_code
    idpel1 = ''
    idpel2 = ''
    idpel3 = ''

    if server_group == 'telepon':
        # Telepon & Speedy Group
        idpel1 = instance.customer[:3] 
        idpel2 = instance.customer[3:]

    elif server_group == 'pln':
        # PLN Reguler
        idpel1 = instance.customer

    elif server_group == 'token-pln':
        # Token PLN
        product = 'PLNPRAB'
        if len(instance.customer) == 11:
            idpel1 = instance.customer
        else :
            idpel2 = instance.customer

    payload = {
        "method"      : "rajabiller.inq",
        "uid"         : _uid,
        "pin"         : _key,
        "idpel1"      : idpel1,
        "idpel2"      : idpel2,
        "idpel3"      : idpel3,
        "kode_produk" : product,
        "ref1"        : instance.trx_code,
    }

    if created:
        if instance.subtype == 'INQ':
            # Request Inquery
            inq_res_obj = InqueryResponse.objects.create(
                trx = instance
            )

            try :
                r = requests.post(url=_url, data=json.dumps(payload), timeout=15)
                if r.status_code == requests.codes.ok:
                    rson = r.json()

                r.raise_for_status()

                inq_res_obj.kode_produk = rson.get('KODE_PRODUK','')
                inq_res_obj.waktu = rson.get('WAKTU','')
                inq_res_obj.idpel1 = rson.get('IDPEL1','')
                inq_res_obj.idpel2 = rson.get('IDPEL2','')
                inq_res_obj.idpel3 = rson.get('IDPEL3','')
                inq_res_obj.nama_pelanggan = rson.get('NAMA_PELANGGAN','')
                inq_res_obj.periode = rson.get('PERIODE','')
                inq_res_obj.nominal = int(rson.get('NOMINAL',0))
                inq_res_obj.admin = int(rson.get('ADMIN',''))
                inq_res_obj.ref1 = rson.get('REF1','')
                inq_res_obj.ref2 = rson.get('REF2','') 
                inq_res_obj.ref3 = rson.get('REF3','') 
                inq_res_obj.status = rson.get('STATUS','') 
                inq_res_obj.ket = rson.get('KET','') 
                inq_res_obj.saldo_terpotong = int(rson.get('SALDO_TERPOTONG',0)) 
                inq_res_obj.sisa_saldo = int(rson.get('SISA_SALDO',''))
                inq_res_obj.url_struk = rson.get('URL_STRUK','') 
                inq_res_obj.save()

            except:
                pass

        else:
            # Request Payment
            pay_res_obj = PaymentResponse.objects.create(
                trx = instance
            )

            # Create Initial Profit
            profit_obj = Profit()
            profit_obj.ppob_trx = instance
            profit_obj.buyer = instance.user
            if instance.user.profile.leader.profile_type == 1:
                profit_obj.leader = instance.user.profile.leader.user
                profit_obj.commision = instance.commision
            profit_obj.save()

            # Initial Billing
            Billing.objects.create(
                ppob_trx = instance, user = instance.user,
                credit = instance.price
            )
            
            # Prev Respose Query
            inq = instance.inquery.trx_inq

            payload["method"] = "rajabiller.paydetail"
            payload["ref1"] = inq.trx.trx_code
            payload["ref2"] = inq.ref2
            payload["nominal"] = inq.nominal
            payload["ref3"] = ""

            if instance.product.nominal > 0:
                payload["nominal"] = instance.product.nominal

            try :
                r = requests.post(url=_url, data=json.dumps(payload), timeout=15)
                if r.status_code == requests.codes.ok:
                    rson = r.json()

                r.raise_for_status()
                pay_res_obj.kode_produk = rson.get('KODE_PRODUK','')
                pay_res_obj.waktu = rson.get('WAKTU','')
                pay_res_obj.idpel1 = rson.get('IDPEL1','')
                pay_res_obj.idpel2 = rson.get('IDPEL2','')
                pay_res_obj.idpel3 = rson.get('IDPEL3','')
                pay_res_obj.nama_pelanggan = rson.get('NAMA_PELANGGAN','')
                pay_res_obj.periode = rson.get('PERIODE','')
                pay_res_obj.nominal = int(rson.get('NOMINAL',0))
                pay_res_obj.admin = int(rson.get('ADMIN',0))
                pay_res_obj.ref1 = rson.get('REF1','')
                pay_res_obj.ref2 = rson.get('REF2','')
                pay_res_obj.ref3 = rson.get('REF3','')
                pay_res_obj.status = rson.get('STATUS','')
                pay_res_obj.ket = rson.get('KET','')
                pay_res_obj.saldo_terpotong = int(rson.get('SALDO_TERPOTONG',0))
                pay_res_obj.sisa_saldo = int(rson.get('SISA_SALDO',0))
                pay_res_obj.url_struk = rson.get('URL_STRUK','')
                pay_res_obj.detail = str(rson.get('DETAIL',''))
                pay_res_obj.save()

                instance.status = instance.PROCESS
                instance.save()
                
            except:
                pass