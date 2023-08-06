from flask import render_template, request, redirect, abort, session
from flask import jsonify
from . import app, db
from .utils import get_payment_url, verify_transaction
from core.models import User, Product, Transaction

fail_code = 7
success_code = 2


@app.route("/", methods=["GET", ])
def product_page():
    products = Product.query.all()
    return render_template("main/product-list.html", products=products)


@app.route("/product-detail/<pk>/", methods=["GET", ])
def product_detail_page(pk):
    product = Product.query.filter_by(id=pk).first()
    if product is None:
        raise abort(404)

    return render_template("main/product-detail.html", product=product)


@app.route("/product/checkout/", methods=["POST", "GET"])
def checkout_page():
    product_id = request.args.get("product_id", None)
    if not product_id:
        abort(403)

    product = Product.query.filter_by(id=product_id).first()
    # Getting the first product by filtering through Id 
    if not product:
        raise abort(404)

    if request.method == "POST":
        data = request.form.to_dict()
        name = data.get("fullName")
        email = data.get("email")
        address = data.get("address")
        city = data.get("city")
        country = data.get("country")
        phone = data.get("phone")
        zip_code = data.get("zip_code")
        # Here we are getting the data from our HTML Form

        transaction_inst = Transaction(
            customer_name=name, customer_email=email, customer_address1=address, customer_address2=address,
            customer_city=city, customer_state=country, customer_country=country, customer_postcode=zip_code, customer_phone=phone, 
            currency="BDT", amount=product.price, product_id=product.id)
        
        # Creating a Transaction Model via the data we recieved

        db.session.add(transaction_inst)
        db.session.commit()
  
        resp, stat_code = get_payment_url(transaction_inst, product)
        # here we are getting the payment url and the status code from utils
        if stat_code != 200:
            raise abort(403, error=resp)
        
        return redirect(resp["payment_url"])
        # later redirecting it to payment url if our status code is 200
    
    return render_template("main/checkout/checkout.html", product=product)
    # will render a checkout template if not a post request


@app.route("/checkout/success/", methods=["POST", ])
def success_page():
    data = request.values.to_dict()
    transaction_id = data.get("mer_txnid")
    if not transaction_id:
        raise abort(404, error=data)
    
    # getting the merchant_txnid if we get from the response 
    # this mer_txnid is the transaction_id we are sending it to the PG
    
    transaction_inst = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if transaction_inst is None:
        raise abort(404)
    
    search_data = verify_transaction(transaction_id)
    # via we are verifying client's transaction

    pg_status_code = int(search_data.get("status_code"))
    if pg_status_code != success_code:
        raise abort(403)
    
    # comparing it with the status code received and PG's status code

    transaction_inst.pg_txnid = data.get("pg_txnid")
    transaction_inst.epw_txnid = data.get("epw_txnid")
    transaction_inst.card_type = data.get("card_type")
    transaction_inst.pg_service_charge_bdt = data.get("pg_service_charge_bdt")
    transaction_inst.card_number = data.get("card_number")
    transaction_inst.bank_txn = data.get("bank_txn")

    # Finally after verification storing all of the data to our database

    db.session.commit()

    return render_template("main/checkout/success.html")


@app.route("/checkout/failure/", methods=["POST", ])
def failure_page():
    data = request.values.to_dict()
    transaction_id = data.get("mer_txnid", None)
    if not transaction_id:
        raise abort(403, error=data)
    
    transaction_inst = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if transaction_inst is None:
        raise abort(404)
    

    search_data = verify_transaction(transaction_id)

    pg_status_code = int(search_data.get("status_code"))
    if pg_status_code != fail_code:
        raise abort(403)
    
    transaction_inst.pg_txnid = data.get("pg_txnid")
    transaction_inst.epw_txnid = data.get("epw_txnid")
    transaction_inst.card_type = data.get("card_type")
    transaction_inst.pg_service_charge_bdt = data.get("pg_service_charge_bdt")
    transaction_inst.card_number = data.get("card_number")
    transaction_inst.bank_txn = data.get("bank_txn")

    db.session.commit()

    return render_template("main/checkout/failure.html")


@app.route("/checkout/cancel/", methods=["POST", "GET"])
def cancel_page():
    if request.method == "POST":
        print("Inside Cancel")
        data = request.values.to_dict()
        print("data received ", data)
        transaction_id = data["mer_txnid"]
        transaction_inst = Transaction.query.filter_by(transaction_id=transaction_id).first()
        if transaction_inst is None:
            raise abort(404)
        
        transaction_inst.pg_txnid = data.get("pg_txnid")
        transaction_inst.epw_txnid = data.get("epw_txnid")
        transaction_inst.card_type = data.get("card_type")
        transaction_inst.pg_service_charge_bdt = data.get("pg_service_charge_bdt")
        transaction_inst.card_number = data.get("card_number")
        transaction_inst.bank_txn = data.get("bank_txn")

        db.session.commit()

    return render_template("main/checkout/cancel.html")