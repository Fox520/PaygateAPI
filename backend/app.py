from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields

# import resources
from endpoints.paygate import PaygateAPI

app = Flask(__name__, static_url_path="")
api = Api(app)

api.add_resource(PaygateAPI, "/api/<string:action>")

if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
