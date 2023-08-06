import os
import json
import requests
from flask import url_for, request
from dotenv import load_dotenv

env = load_dotenv(".env")
print(env)


def get_payment_url(transaction_inst, product):
    payload = {
        "store_id": os.getenv("AAMARPAY_STORE_ID"),
        "signature_key": os.getenv("AAMARPAY_SIGNATURE_KEY"),
        "tran_id": transaction_inst.transaction_id,

        "success_url": "{}{}".format(request.url_root[:-1], url_for("success_page")),
        "fail_url": "{}{}".format(request.url_root[:-1], url_for("failure_page")),
        "cancel_url": "{}{}".format(request.url_root[:-1], url_for("cancel_page")),

        "amount": product.price,
        "currency": "BDT",
        "cus_name": transaction_inst.customer_name,
        "cus_email": transaction_inst.customer_email,
        "cus_add1": transaction_inst.customer_address1,
        "cus_add2": transaction_inst.customer_address2,
        "cus_city": transaction_inst.customer_city,
        "cus_state": transaction_inst.customer_state,
        "cus_postcode": transaction_inst.customer_postcode,
        "cus_country": transaction_inst.customer_country,
        "cus_phone": transaction_inst.customer_phone,
        "desc": "Flask User",
        "type": "json"
    }
    data = json.dumps(payload)

    url = "https://sandbox.aamarpay.com/jsonpost.php"

    r = requests.post(url, data=data)
    res_data = r.json()
    result = res_data.get("result", None)
    if not result:
        r.status_code = 400
    
    return res_data, r.status_code


def verify_transaction(merchant_id):
    store_id = os.getenv("AAMARPAY_STORE_ID")
    signature_key = os.getenv("AAMARPAY_SIGNATURE_KEY")
    url = f"http://sandbox.aamarpay.com/api/v1/trxcheck/request.php?request_id={merchant_id}&store_id={store_id}&signature_key={signature_key}&type=json"
    r = requests.get(url)
    return r.json()
