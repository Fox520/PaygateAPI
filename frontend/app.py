import string
import random
import requests
import json
from flask import Flask, render_template, flash, url_for, redirect, request, make_response, jsonify
from forms import DetailsForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "1a5727507bf3f1bcd3d8a213ff453de1"

API_URL = "http://fox520.duckdns.org:5001/api"
RETURN_URL = "http://fox520.duckdns.org:5000/final"
PAYGATE_REDIRECT_URL = "https://secure.paygate.co.za/payweb3/process.trans"
TRANSACTION_STATUS = {
    "0": "Not Done",
    "1": "Approved",
    "2": "Declined",
    "3": "Cancelled",
    "4": "User Cancelled",
    "5": "Received by PayGate",
    "7": "Settlement Voided"
}


def random_text(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

@app.route("/", methods=["GET", "POST"])
@app.route("/home")
def hello():
    form = DetailsForm()
    resp = make_response(render_template("home.html", forms=form))
    if form.validate_on_submit():
        # identifies the current user purchase
        ref = random_text(20)
        resp.set_cookie("reference", ref)
        req = {
            "package": request.form["package"],
            "order_info": {
                "phone_number": request.form["phone_number"],
                "airtime_amount": request.form["airtime_amount"]
            },
            
            "pay_method": request.form["pay_method"],
            "email": request.form["email"],
            "amount": str(float("5.50")*100),
            "currency": "NAD",
            "return_url": RETURN_URL,
            "locale": "en",
            "country": "NAM",
            "reference": ref
        }
        # Send request to our api
        data = json.loads(requests.post(API_URL+"/initiate", json=req).text)
        if data.get("error"):
            flash(data["error"], "warning")
            print(data['error'])
            # Remove cookie
            resp.set_cookie('reference', '', expires=0)
            return resp
        pri = data["PAY_REQUEST_ID"]
        checksum = data["CHECKSUM"]
        return redirect(url_for('gateway', a=pri,b=checksum), code=307)

    return resp


@app.route("/gateway", methods=["POST", "GET"])
def gateway():
    return render_template("gateway.html", a=request.args["a"], b=request.args["b"])

@app.route("/final", methods=["POST", "GET"])
def final():
    data = request.form
    result_desc = TRANSACTION_STATUS[data["TRANSACTION_STATUS"]]
    params1 = {"pay_request_id":data["PAY_REQUEST_ID"]}
    reference = requests.get(API_URL+"/ref", params=params1).text
    params2 = {"reference": reference}
    payment_data = json.loads(requests.get(API_URL+"/payment-data",params=params2).text)

    # Check if transaction was successful
    if data["TRANSACTION_STATUS"] == "1":
        # contact api to fulfill transaction
        params3 = {"reference": reference}
        result = json.loads(requests.get(API_URL+"/complete-purchase",params=params3).text)
    return render_template("final.html", data=data, result_desc=result_desc, payment_data=payment_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
