from flask import render_template, request, redirect, abort, session
from flask import jsonify
from . import app, db
from .utils import get_payment_url, search_transaction
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

        transaction_inst = Transaction(customer_name=name, customer_email=email, customer_address1=address, customer_address2=address,
            customer_city=city, customer_state=country, customer_country=country, customer_postcode=zip_code, customer_phone=phone, 
            currency="BDT", amount=product.price, product_id=product.id)

        db.session.add(transaction_inst)
        db.session.commit()
  
        resp = get_payment_url(transaction_inst, product)
        return redirect(resp["payment_url"])
    
    return render_template("main/checkout/checkout.html", product=product)


@app.route("/checkout/success/", methods=["POST", ])
def success_page():
    print("Inside Success")
    data = request.values.to_dict()
    print("data received ", data)
    transaction_id = data["mer_txnid"]
    transaction_inst = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if transaction_inst is None:
        raise abort(404)
    
    search_data = search_transaction(transaction_id)

    pg_status_code = int(search_data.get("status_code"))
    if pg_status_code != success_code:
        raise abort(403)

    transaction_inst.pg_txnid = data.get("pg_txnid")
    transaction_inst.epw_txnid = data.get("epw_txnid")
    transaction_inst.card_type = data.get("card_type")
    transaction_inst.pg_service_charge_bdt = data.get("pg_service_charge_bdt")
    transaction_inst.card_number = data.get("card_number")
    transaction_inst.bank_txn = data.get("bank_txn")

    db.session.commit()

    return render_template("main/checkout/success.html")


@app.route("/checkout/failure/", methods=["POST", ])
def failure_page():
    print("Inside Failure")
    data = request.values.to_dict()
    print("data received ", data)
    transaction_id = data["mer_txnid"]
    transaction_inst = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if transaction_inst is None:
        raise abort(404)
    

    search_data = search_transaction(transaction_id)

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


@app.route("/checkout/cancel/", methods=["POST", ])
def cancel_page():
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