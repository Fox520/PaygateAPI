import os
import json
import hashlib
import requests
from datetime import datetime
from flask import Flask, jsonify
from flask import request
from flask_restful import Api, Resource

app = Flask(__name__, static_url_path="")
api = Api(app)

PAYGATE_ID = 10011072130
ENCRYPTION_KEY = "secret"
INITIATE_URL = "https://secure.paygate.co.za/payweb3/initiate.trans"

# reference: {PAY_REQUEST_ID, checksum}
important_data = {}
pyi_to_ref = {}

# reference is key
# contains everything data the form
payment_data = {}


class PaygateAPI(Resource):
    def __init__(self):
        super(PaygateAPI, self).__init__()

    def get(self, action):
        if action == "payment-data":
            ref = request.args.get("reference")
            if ref is None:
                return ""
            ref = json.loads(ref)
            return jsonify(payment_data.get(ref))
        elif action == "ref":
            k = request.args.get("pay_request_id", "-1")
            # Returns the reference based on the pay request id given; -1 if not found
            return pyi_to_ref.get(str(k))
        elif action == "complete-purchase":
            ref = request.args.get("reference")
            if ref is None:
                return ""
            ref = json.loads(ref)
            if payment_data.has_key(ref):
                return jsonify(self.complete_purchase(ref))
            else:
                return jsonify({"result": False, "reason": "Reference not found."})

    def post(self, action):
        if action == "initiate":
            print(request.headers)
            return jsonify(self.initiate_payment(request.get_json(force=True)))

    def initiate_payment(self, args):
        # Ensure reference does not already exist
        if args["reference"] not in important_data:
            ref = args["reference"]
            api_request = {
                "PAYGATE_ID": str(PAYGATE_ID),
                "REFERENCE": ref,
                "AMOUNT": "3299",  # args["amount"],
                "CURRENCY": "ZAR",  # args["currency"],
                "RETURN_URL": args["return_url"],
                "TRANSACTION_DATE": utc_now(),
                "LOCALE": "en-za", #args["locale"],
                "COUNTRY": "ZAF",  # args["country"],
                "EMAIL": args["email"],
                "PAY_METHOD": "CC",  # args["pay_method"]
            }
            api_request["CHECKSUM"] = get_checksum(api_request, ENCRYPTION_KEY)

            # Send request to paygate api
            r = requests.post(INITIATE_URL, data=api_request)
            # Convert result to dictionary
            result = format_response(r.text)
            # determine if error occured
            if result[0]:
                important_data[ref] = {
                    "PAY_REQUEST_ID": result[1]["PAY_REQUEST_ID"],
                    "CHECKSUM": api_request["CHECKSUM"],
                }
                pyi_to_ref[result[1]["PAY_REQUEST_ID"]] = args.pop("reference")
                # Store posted data
                payment_data[ref] = args
                # print(important_data)
                # print(pyi_to_ref)
                # print("\n")
                return result[1]
            else:
                return {"error": result[1]}

        else:
            return {"result": False, "reason": "Reference already exists"}

    def complete_purchase(self, reference: str):
        # contact internal api here
        return {"result": True}


def format_response(r):
    # PAYGATE_ID=10011072130&PAY_REQUEST_ID=CBE59FBB-003A-58BB-6494-294BF0E7103D&REFERENCE=C78Z6T2V30QTODYK315Z&CHECKSUM=7cbe02f38a4bdbbae6d7a9f7a4e0981e
    fin = {}
    for p in [x.split("=") for x in r.split("&")]:
        fin[p[0]] = p[1]
    if len(fin) == 1:
        # error
        return (False, r.split("=")[1])
    return (True, fin)


def get_checksum(data: dict, key: str):
    data = "".join([str(x) for x in data.values()]) + key
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def utc_now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
