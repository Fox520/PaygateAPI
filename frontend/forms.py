from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Email, InputRequired

PACKAGE_CHOICES = [
    ("airtime", "Airtime"),
    ("mobile_data", "Mobile data"),
    ("turbo_boost", "TurboBoost"),
    ("invoice_payment", "Invoice payment"),
    ("handset", "Handset"),
    ("prepayments", "Prepayments"),
]
PAYMENT_METHOD_CHOICES = [
    ("CC", "Credit Card"),
    ("DC", "Debit Card"),
    ("EW", "E-Wallet"),
    ("BT", "Bank Transfer"),
    ("CV", "Cash Voucher"),
    ("PC", "Pre-Paid Card"),
]


class DetailsForm(FlaskForm):
    package = SelectField(
        u"Package", choices=PACKAGE_CHOICES, validators=[InputRequired()]
    )
    phone_number = StringField("Phone number", validators=[InputRequired()])
    phone_name = StringField("Handset name")
    pay_method = SelectField(
        u"Payment method", choices=PAYMENT_METHOD_CHOICES, validators=[InputRequired()]
    )
    quantity = StringField("Quantity", validators=[InputRequired()])
    email = StringField("E-mail address", validators=[InputRequired(), Email()])
    submit = SubmitField("Proceed to checkout")
