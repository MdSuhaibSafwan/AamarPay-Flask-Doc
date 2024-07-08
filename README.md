# AamarPay-Flask-Documentation

This is a demo made for AamarPay of using their API in Python using Flask.
This repo can be cloned to make it work by inputing the environment variables and using your onw business logic. For simplicity we have put a product which was created by admin before and user can only purchase it using a simple API.

In the checkout page we took the details of the user and made a transaction there by the function mentioned in the utils "get_payment_url" and using that we make a transaction once the post request is made to aamarpay API we get a url from it and further redirect the user to it.

Next in the aamarpay endpoint the transaction can be marked in either one of the three,
1. Success,
2. Failure,
3. Cancelled

Once the transaction is made and marked as either one of three Aamarpay sends a post request to our endpoint(API)
For this we have made 3 endpoints of success, failure and cancelled to it and the function "verify_transaction" handles the rest using the merchant id provided by us.

This is a boiler plate to integrate aamarpay api in the quickly in any python template for more information checkout the link,
https://aamarpay.readme.io/reference/initiate-payment-json
