# PaygateAPI
 
## Running the api
```
python3 -m pip install flask flask_restful requests
cd backend
python3 app.py
```

## How to interact
### Initiating a transaction
```
POST to http://API_URL/api/initiate
BODY
{
    "ref": String, # Randomly string to identify the user
    "amount": String, #amount to charge; format: $5.99 is x100 therefore 599
    "return_url": String, # After user completes/cancels payment
    "email": String,
    "pay_method": "CC", # method of payment
    "order_info": # e.g. {'purchase_type': 'airtime', 'quantity': 10, ...}
}

RESPONSE
{
    "PAYGATE_ID": int,
    "PAY_REQUEST_ID": String,
    "REFERENCE": String, # Same as the one in POST reqeust
    "CHECKSUM":String
}

```
### Redirect to Paygate
```php
// Example
<form action="https://secure.paygate.co.za/payweb3/process.trans" method="POST" >
    <input type="hidden" name="PAY_REQUEST_ID" value="23B785AE-C96C-32AF-4879-D2C9363DB6E8">
    <input type="hidden" name="CHECKSUM" value="b41a77f83a275a849f23e30b4666e837">
</form>

```
### Then
```
PayWeb redirects the client back to the 'return_url' provided in the initiate phase.
More here: http://docs.paygate.co.za/#return-to-merchant
```

### Retrieving reference from a PAY_REQUEST_ID
```
GET to http://API_URL/api/ref?pay_request_id=xyz

RESPONSE is plain/text however if response is "-1" it means
the pay_request_id was not found.
```

### Retrieving the order information
```
GET to http://API_URL/api/payment-data?reference=abc

RESPONSE application/json of all from initiation phase excluding reference, e.g.
{
    "amount": String, #amount to charge; format: $5.99 is x100 therefore 599
    "return_url": String, # After user completes/cancels payment
    "email": String,
    "pay_method": "CC", # method of payment
    "order_info": # e.g. {'purchase_type': 'airtime', 'quantity': 10, ...}
}
```