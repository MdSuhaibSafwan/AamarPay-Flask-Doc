from flask import render_template, request, redirect
from flask import jsonify
from . import app
from .utils import get_payment_url

@app.route("/", methods=["GET", ])
def index_page():

    return render_template("main/index.html")


@app.route("/products/", methods=["GET", ])
def product_page():

    return render_template("main/product-list.html")


@app.route("/product-detail/<pk>/", methods=["GET", ])
def product_detail_page(pk):
    print("pk ", pk)

    return render_template("main/product-detail.html")


@app.route("/product/checkout/", methods=["POST", "GET"])
def checkout_page():
    if request.method == "POST":
        

        return redirect()


    return render_template("main/checkout/checkout.html", )


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