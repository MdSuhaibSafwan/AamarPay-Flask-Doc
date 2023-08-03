from flask import render_template, request, redirect, abort
from flask import jsonify
from . import app
from .utils import get_payment_url
from core.models import User, Product, Transaction


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
    if request.method == "POST":
        

        return redirect()

    product_id = request.args.get("product_id", None)
    if not product_id:
        abort(403)

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        raise abort(404)

    return render_template("main/checkout/checkout.html", product=product)


@app.route("/checkout/success/", methods=["POST", "GET"])
def success_page():
    data = request.values.to_dict()
    print("data received ", data)

    return render_template("main/checkout/success.html")


@app.route("/checkout/failure/", methods=["POST", ])
def failure_page():
    data = request.values.to_dict()
    print("data received ", data)

    return render_template("main/checkout/failure.html")


@app.route("/checkout/cancel/", methods=["POST", ])
def cancel_page():
    data = request.values.to_dict()
    print("data received ", data)

    return render_template("main/checkout/cancel.html")