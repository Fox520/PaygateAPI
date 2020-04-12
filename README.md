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
    "return_url": String,# After user completes/cancels payment
    "email": args["email"],
    "pay_method": "CC", # method of payment
    "order_info": # e.g. {'purchase_type': 'airtime', 'quantity': 10, ...}
}

```