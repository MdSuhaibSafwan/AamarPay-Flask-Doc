import os
import requests

def get_payment_url(data: dict):
    data["store_id"] = os.getenv("AAMARPAY_STORE_ID")
    data["tran_id"] = os.getenv("AAMARPAY_SIGNATURE_KEY")
    
    url = "https://​sandbox​.aamarpay.com/jsonpost.php"

    requests.post(url, data=data)

