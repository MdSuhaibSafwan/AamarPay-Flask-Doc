from flask import render_template, request
from flask import jsonify
from . import app


@app.route("/", methods=["GET", ])
def index_page():

    return render_template("main/index.html")


@app.route("/products/", methods=["GET", ])
def product_page():

    return render_template("main/products.html")



@app.route("/products/add-product/", methods=["POST", ])
def add_product_to_cart():
    lst = [
        {
            "name": "AamarPay",
        },
    ]

    return jsonify(lst)


@app.route("/checkout/success/", methods=["POST", ])
def success_page():
    data = request.get_json()
    print(data)
    return render_template("main/success.html")


@app.route("/checkout/failure/", methods=["POST", ])
def failure_page():
    data = request.get_json()
    print(data)

    return render_template("main/failure.html")


@app.route("/checkout/cancel/", methods=["POST", ])
def cancel_page():
    data = request.get_json()
    print(data)

    return render_template("main/cancel.html")